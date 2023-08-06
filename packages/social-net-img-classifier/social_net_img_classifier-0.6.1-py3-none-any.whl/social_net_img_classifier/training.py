import keras.engine.sequential
import numpy as np
import pandas as pd
import optuna
import langid
from lightgbm import LGBMClassifier
from statistics import mode
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import backend
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

from social_net_img_classifier.settings import FEATURES, LANGUAGES
from social_net_img_classifier.utils import NlpUtils


langid.set_languages(LANGUAGES)
TARGET = "target"
AVG_METRIC = "macro"


class TrainClassModel:
    """
    :Date: 2022-08-29
    :Version: 0.3.1
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: ENTRENAR MODELO QUE PERMITE CLASIFICAR UNA VARIABLE CATEGÓRICA A PARTIR DE VARIABLES NUMÉRICAS
    """
    def __init__(self, input_df, features=FEATURES, val_size=0.2, balance="oversampling", drop_duplicates=True):
        """
        :Description: inicializar proceso y hacer división de grupo de entrenamiento/pruebas
        :param input_df: tabla de entrada.
               Debe incluir una var. objetivo y vars. independientes numéricas (:type: pd.DataFrame)
        :param features: lista de variables independientes numéricas (:type: list)
        :param val_size: tamaño porcentual del grupo de prueba -entre 0 y 1- (:type: float)
        :param balance: "oversampling", "undersampling" o None (:type: string)
        :param drop_duplicates: -verdadero- se eliminan registros duplicados (:type: boolean)
        """
        df = input_df[features].fillna(0)
        df[TARGET] = input_df[TARGET]
        df_train, df_test = self.data_split(df, val_size, balance, drop_duplicates)
        self.X_train = df_train[features]
        self.Y_train = df_train[TARGET]
        self.X_test = df_test[features]
        self.Y_test = df_test[TARGET]
        self.vz = val_size
        self.best_params = None

    def fit_best_model(self, n_trials=100, n_splits=5, model_type="logit", metric="f1"):
        """
        :Description: entrenar y ajustar el mejor* modelo
        :param n_trials: número de combinaciones de hiperparámetros a probar (:type: int)
        :param n_splits: número de "folds" para "cross-validation" (:type: int)
        :param metric: métrica a optimizar -"f1" o "accuracy"- (:type: string)
        :param model_type: nombre del modelo a entrenar -"random_forest", "svm", "lgbm", "deep_nn"- (:type: string)
        :return: mejor modelo obtenido; mejores métricas sobre entrenamiento, validación y prueba
        """
        self.mt = model_type
        self.metric = metric
        model, train_metric, val_metric = self.train(n_trials=n_trials, n_splits=n_splits)
        print(f"*** MODEL: {self.mt} ***")
        print(f"train metric -{self.metric}-: {train_metric}")
        print(f"validation metric -{self.metric}-: {val_metric}")
        pred = self.predict(model, self.X_test)
        if self.metric == "f1":
            test_metric = metrics.f1_score(self.Y_test, pred, average=AVG_METRIC)
        else:
            test_metric = metrics.accuracy_score(self.Y_test, pred)
        print(f"test metric -{self.metric}-: {test_metric}")
        print("Confusion Matrix for test set")
        print(metrics.classification_report(self.Y_test, pred))
        print(metrics.confusion_matrix(self.Y_test, pred))
        return model, train_metric, val_metric, test_metric

    @staticmethod
    def data_split(dataset, test_size, balance="oversampling", drop_duplicates=True):
        """
        :Description: separar un conjunto de datos en conjuntos de entrenamiento y prueba
        :param dataset: conjunto de datos (:type: pd.DataFrame)
        :param test_size: tamaño del conjunto de prueba -de 0 a 1- (:type: float)
        :param balance: "oversampling", "undersampling" o None (:type: string)
        :param drop_duplicates: -verdadero- se eliminan registros duplicados (:type: boolean)
        :return: conjunto de entrenamiento y conjunto de prueba (:type: pandas.DataFrame)
        """
        if drop_duplicates is True:
            df = dataset.drop_duplicates()
            print(f"{len(dataset)-len(df)} duplicated rows removed")
        else:
            df = dataset.copy()
        if balance == "undersampling":
            min_freq = min(pd.value_counts(df[TARGET]).to_frame()[TARGET].to_list())
            train_freq = int(round((1 - test_size) * min_freq, 0))
            df_train = pd.concat(
                [resample(df[df[TARGET] == c], replace=False, n_samples=train_freq) for c in df[TARGET].unique()])
            df_test = df.merge(df_train, on=df_train.columns.to_list(), how='left', indicator=True)
            df_test = df_test.loc[df_test["_merge"] == 'left_only', df_test.columns != '_merge']
            print(f"Dataset balanced ONLY for training.")
        elif balance == "oversampling":
            df_train, df_test = train_test_split(df, test_size=test_size, stratify=df[TARGET])
            X, y = df_train[df_train.columns.difference([TARGET])], df_train[TARGET]
            X, y = SMOTE().fit_resample(X, y)
            df_train = pd.concat([X, y], axis=1)
            print(f"Dataset balanced ONLY for training.")
        else:
            df_train, df_test = train_test_split(df, test_size=test_size, stratify=df[TARGET])
        print(f"training set size: {len(df_train)} | test set size: {len(df_test)}")
        print(f"{TARGET} for training set:\n"
              f"{df_train[TARGET].value_counts()}")
        print(f"{TARGET} for test set:\n"
              f"{df_test[TARGET].value_counts()}")
        return df_train, df_test

    def train(self, n_trials=50, n_splits=5):
        self.optimize(n_trials)
        cv_model, metric_tr, metric_val = self.cv_model(n_splits)
        return cv_model, metric_tr, metric_val

    def optimize(self, n_trials=50):
        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=n_trials)
        print('Number of finished trials:', len(study.trials))
        print('Best trial:', study.best_trial.params)
        self.best_params = study.best_params

    def objective(self, trial):
        train_x, test_x, train_y, test_y = train_test_split(self.X_train, self.Y_train, test_size=self.vz)
        if self.mt == "random_forest":
            param = {
                'n_estimators': trial.suggest_int('n_estimators', 25, 75, step=10),
                'max_features': 'sqrt',
                'max_depth': trial.suggest_categorical('max_depth', [None, 10, 12, 14]),
                'min_samples_split': trial.suggest_categorical('min_samples_split', [3, 4, 5]),
                'min_samples_leaf': trial.suggest_categorical('min_samples_leaf', [2, 3, 4]),
                'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
                'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy'])
            }
            model = RandomForestClassifier(**param)
            model.fit(train_x, train_y)
        elif self.mt == "svm":
            param = {
                'C': trial.suggest_categorical('C', [1, 2, 3, 5, 8, 10, 15, 20, 25, 40, 60, 80, 100]),
                'shrinking': trial.suggest_categorical('shrinking', [True, False]),
                'kernel': trial.suggest_categorical('kernel', ["poly", "rbf", "sigmoid"])
            }
            model = SVC(**param)
            model.fit(train_x, train_y)
        elif self.mt == "lgbm":
            param = {
                'learning_rate': trial.suggest_categorical('learning_rate', [.04, .05, .06, .07, .08, .09, .1]),
                'n_estimators': trial.suggest_int('n_estimators', 20, 60),
                'max_depth': trial.suggest_int('max_depth', 10, 20),
                'colsample_bytree': trial.suggest_categorical('colsample_bytree', [.65, .7, .75, .8]),
                'reg_alpha': trial.suggest_loguniform('reg_alpha', .1, .4),
                'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-3, .5),
                'min_child_samples': trial.suggest_int('min_child_samples', 5, 15),
            }
            model = LGBMClassifier(**param)
            model.fit(train_x, train_y)
        elif self.mt == "deep_nn":
            param = {
                "dense_layers": trial.suggest_int("dense_layers", 1, 8, step=1),
                "neurons_by_layer": trial.suggest_int("neurons_by_layer", 2, 8, step=1),
                "activation": trial.suggest_categorical("activation", ["tanh", "relu"]),
                "dropout_rate": trial.suggest_categorical("dropout_rate", [.1, .15, .2, .25, .3, .35, .4]),
            }
            n_features = train_x.shape[1]
            n_classes = len(set(train_y))
            encoder = LabelEncoder().fit(train_y)
            train_y = to_categorical(encoder.transform(train_y))
            model = NNclf().baseline(n_features=n_features, n_classes=n_classes, metric=self.metric, **param)
            model.fit(train_x, train_y, epochs=100, verbose=False)
            model.classes_ = encoder.classes_
        else:
            param = {
                'penalty': trial.suggest_categorical('penalty', ['none', 'l2']),
            }
            model = LogisticRegression(**param)
            model.fit(train_x, train_y)
        if isinstance(model, keras.engine.sequential.Sequential):
            preds = NNclf().predict(model, self.X_test)
        else:
            preds = model.predict(self.X_test)
        if self.metric == "f1":
            metric = metrics.f1_score(self.Y_test, preds, average=AVG_METRIC)
        else:
            metric = metrics.accuracy_score(self.Y_test, preds)
        return metric

    def cv_model(self, n_splits=5):
        kf = KFold(n_splits=n_splits, random_state=48, shuffle=True)
        cv_model, scores_tr, scores_val = [], [], []
        n = 0
        for trn_idx, test_idx in kf.split(self.X_train, self.Y_train):
            X_tr = self.X_train.iloc[trn_idx]
            X_val = self.X_train.iloc[test_idx]
            y_tr = self.Y_train.iloc[trn_idx]
            y_val = self.Y_train.iloc[test_idx]
            if self.mt == "random_forest":
                model = RandomForestClassifier(**self.best_params)
                model.fit(X_tr, y_tr)
            elif self.mt == "svm":
                model = SVC(**self.best_params)
                model.fit(X_tr, y_tr)
            elif self.mt == "lgbm":
                model = LGBMClassifier(**self.best_params)
                model.fit(X_tr, y_tr)
            elif self.mt == "deep_nn":
                n_features = X_tr.shape[1]
                n_classes = len(set(y_tr))
                encoder = LabelEncoder().fit(y_tr)
                y_tr_cat = to_categorical(encoder.transform(y_tr))
                model = NNclf().baseline(n_features=n_features, n_classes=n_classes, metric=self.metric,
                                         **self.best_params)
                model.fit(X_tr, y_tr_cat, epochs=200, verbose=False)
                model.classes_ = encoder.classes_
            else:
                model = LogisticRegression(**self.best_params)
                model.fit(X_tr, y_tr)

            cv_model.append(model)
            if isinstance(model, keras.engine.sequential.Sequential):
                preds_tr = NNclf().predict(model, X_tr)
                preds_val = NNclf().predict(model, X_val)
            else:
                preds_tr = model.predict(X_tr)
                preds_val = model.predict(X_val)
            if self.metric == "f1":
                scores_val.append(metrics.f1_score(y_val, preds_val, average=AVG_METRIC))
                scores_tr.append(metrics.f1_score(y_tr, preds_tr, average=AVG_METRIC))
            else:
                scores_val.append(metrics.accuracy_score(y_val, preds_val))
                scores_tr.append(metrics.accuracy_score(y_tr, preds_tr))
            print(f"Fold {n + 1} - {self.metric}: train = {scores_tr[n]}, validation = {scores_val[n]}")
            n += 1
        return cv_model, np.mean(scores_tr), np.mean(scores_val)

    @staticmethod
    def predict(cv_model, X_data):
        preds = []
        for model in cv_model:
            if isinstance(model, keras.engine.sequential.Sequential):
                preds.append(NNclf().predict(model, X_data))
            else:
                preds.append(model.predict(X_data))
        preds = np.array(preds).T.tolist()
        preds = [mode(p) for p in preds]
        return preds


class TrainClfTextModel:
    """
    :Date: 2022-08-26
    :Version: 0.2
    :Author: Joan Felipe Mendoza
    :Description: TRAIN A TEXT CLASIFICATION MODEL OPTIMIZING HYPERPARAMENTERS
    """
    def __init__(self, input_df, text_col, label_col, detect_lang=True, clean_mode="normal", val_size=0.2, balance=None, drop_duplicates=True):
        """
        :description: initialise process and do training/testing group splitting.
        :param input_df: input table.
               Must include a target feature, and a text independent feature. (:type: pd.DataFrame)
        :param text_col: name of column with raw text (:type: string)
        :param label_col: name of column with labels (:type: string)
        :param detect_lang: -True: detect language of text- (:type: boolean)
        :param clean_mode: cleansing pre-processing -'normal', 'stemma', 'lemma' or None-
        :param val_size: percentage size of the test group - between 0 and 1- (:type: float)
        :param balance: undersampling or None (:type: string)
        :param drop_duplicates: -true- duplicate records are removed (:type: boolean)
        """
        self.label = label_col
        df = input_df[[text_col, label_col]]
        if clean_mode:
            clean_texts = []
            for _, row in df.iterrows():
                # Detect language
                if detect_lang:
                    lang, _ = langid.classify(row[text_col])
                else:
                    lang = None
                # Clean text with basic transformations
                clean_txt = NlpUtils().clean_text(str(row[text_col]), lang)
                # Calculate stemmas
                if clean_mode == "stemma":
                    clean_txt = NlpUtils().stem_text(clean_txt, lang)
                # Calculate lemmas
                if clean_mode == "lemma":
                    clean_txt = NlpUtils().lemma_text(clean_txt, lang)
                clean_texts.append(clean_txt)
            df[text_col] = clean_texts
        df_train, df_test = self.data_split(df, val_size, balance, drop_duplicates)
        self.X_train = df_train[text_col]
        self.Y_train = df_train[label_col]
        self.X_test = df_test[text_col]
        self.Y_test = df_test[label_col]
        self.vz = val_size
        self.best_params = None

    def fit_best_model(self, n_trials=100, n_splits=5, model_type="logit", metric="f1"):
        """
        :description: train and fit the best* model
        :param n_trials: number of hyperparameter combinations to test (:type: int)
        :param n_splits: number of "folds" for "cross-validation" (:type: int)
        :param metric: metric to optimise - "f1" or "accuracy" - (:type: string)
        :param model_type: name of the model to be trained - "random_forest", "svm", "lgbm"- (:type: string)
        :return: best model obtained; best metrics on training, validation and test
        """
        self.mt = model_type
        self.metric = metric
        model, train_metric, val_metric = self.train(n_trials=n_trials, n_splits=n_splits)
        print(f"*** MODEL: {self.mt} ***")
        print(f"train metric -{self.metric}-: {train_metric}")
        print(f"validation metric -{self.metric}-: {val_metric}")
        pred = self.predict(model, self.X_test)
        if self.metric == "f1":
            test_metric = metrics.f1_score(self.Y_test, pred, average=AVG_METRIC)
        else:
            test_metric = metrics.accuracy_score(self.Y_test, pred)
        print(f"test metric -{self.metric}-: {test_metric}")
        print("Confusion Matrix for test set")
        print(metrics.classification_report(self.Y_test, pred))
        print(metrics.confusion_matrix(self.Y_test, pred))
        return model, train_metric, val_metric, test_metric

    def data_split(self, dataset, test_size, balance=None, drop_duplicates=True):
        """
        :description: separate a dataset into training and test sets
        :param dataset: dataset (:type: pd.DataFrame)
        :param test_size: size of the test set - from 0 to 1- (:type: float)
        :param balance: undersampling or None (:type: string)
        :param drop_duplicates: -true - duplicate records are removed (:type: boolean)
        :return: training set and test set (:type: pandas.DataFrame)
        """
        if drop_duplicates is True:
            df = dataset.drop_duplicates()
            print(f"{len(dataset)-len(df)} duplicated rows removed")
        else:
            df = dataset.copy()
        if balance == "undersampling":
            min_freq = min(pd.value_counts(df[self.label]).to_frame()[self.label].to_list())
            train_freq = int(round((1 - test_size) * min_freq, 0))
            df_train = pd.concat(
                [resample(df[df[self.label] == c], replace=False, n_samples=train_freq) for c in df[self.label].unique()])
            df_test = df.merge(df_train, on=df_train.columns.to_list(), how='left', indicator=True)
            df_test = df_test.loc[df_test["_merge"] == 'left_only', df_test.columns != '_merge']
            print(f"Dataset balanced ONLY for training.")
        else:
            df_train, df_test = train_test_split(df, test_size=test_size, stratify=df[self.label])
        print(f"training set size: {len(df_train)} | test set size: {len(df_test)}")
        print(f"{self.label} for training set:\n"
              f"{df_train[self.label].value_counts()}")
        print(f"{self.label} for test set:\n"
              f"{df_test[self.label].value_counts()}")
        return df_train, df_test

    def train(self, n_trials=50, n_splits=5):
        self.optimize(n_trials)
        cv_model, metric_tr, metric_val = self.cv_model(n_splits)
        return cv_model, metric_tr, metric_val

    def optimize(self, n_trials=50):
        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=n_trials)
        print('Number of finished trials:', len(study.trials))
        print('Best trial:', study.best_trial.params)
        self.best_params = study.best_params

    def objective(self, trial):
        train_x, test_x, train_y, test_y = train_test_split(self.X_train, self.Y_train, test_size=self.vz)
        if self.mt == "random_forest":
            param = {
                'n_estimators': trial.suggest_int('n_estimators', 25, 75, step=10),
                'max_features': 'sqrt',
                'max_depth': trial.suggest_categorical('max_depth', [None, 10, 12, 14]),
                'min_samples_split': trial.suggest_categorical('min_samples_split', [3, 4, 5]),
                'min_samples_leaf': trial.suggest_categorical('min_samples_leaf', [2, 3, 4]),
                'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
                'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy'])
            }
            model = Pipeline([
                ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                ('clf', RandomForestClassifier(**param))
                ])
            model.fit(train_x, train_y)
        elif self.mt == "svm":
            param = {
                'C': trial.suggest_categorical('C', [1, 2, 3, 5, 8, 10, 15, 20, 25, 40, 60, 80, 100]),
                'shrinking': trial.suggest_categorical('shrinking', [True, False]),
                'kernel': trial.suggest_categorical('kernel', ["poly", "rbf", "sigmoid"])
            }
            model = Pipeline([
                ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                ('clf', SVC(**param))
            ])
            model.fit(train_x, train_y)
        elif self.mt == "lgbm":
            param = {
                'learning_rate': trial.suggest_categorical('learning_rate', [.04, .05, .06, .07, .08, .09, .1]),
                'n_estimators': trial.suggest_int('n_estimators', 20, 60),
                'max_depth': trial.suggest_int('max_depth', 10, 20),
                'colsample_bytree': trial.suggest_categorical('colsample_bytree', [.65, .7, .75, .8]),
                'reg_alpha': trial.suggest_loguniform('reg_alpha', .1, .4),
                'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-3, .5),
                'min_child_samples': trial.suggest_int('min_child_samples', 5, 15),
            }
            model = Pipeline([
                ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                ('clf', LGBMClassifier(**param))
            ])
            model.fit(train_x, train_y)
        else:
            param = {
                'penalty': trial.suggest_categorical('penalty', ['none', 'l2']),
            }
            model = Pipeline([
                ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                ('clf', LogisticRegression(**param))
            ])
            model.fit(train_x, train_y)
        preds = model.predict(self.X_test)
        if self.metric == "f1":
            metric = metrics.f1_score(self.Y_test, preds, average=AVG_METRIC)
        else:
            metric = metrics.accuracy_score(self.Y_test, preds)
        return metric

    def cv_model(self, n_splits=5):
        kf = KFold(n_splits=n_splits, random_state=48, shuffle=True)
        cv_model, scores_tr, scores_val = [], [], []
        n = 0
        for trn_idx, test_idx in kf.split(self.X_train, self.Y_train):
            X_tr = self.X_train.iloc[trn_idx]
            X_val = self.X_train.iloc[test_idx]
            y_tr = self.Y_train.iloc[trn_idx]
            y_val = self.Y_train.iloc[test_idx]
            if self.mt == "random_forest":
                model = Pipeline([
                    ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                    ('clf', RandomForestClassifier(**self.best_params))
                ])
                model.fit(X_tr, y_tr)
            elif self.mt == "svm":
                model = Pipeline([
                    ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                    ('clf', SVC(**self.best_params))
                ])
                model.fit(X_tr, y_tr)
            elif self.mt == "lgbm":
                model = Pipeline([
                    ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                    ('clf', LGBMClassifier(**self.best_params))
                ])
                model.fit(X_tr, y_tr)
            else:
                model = Pipeline([
                    ('tfidf', TfidfVectorizer(sublinear_tf=True, min_df=50, max_df=0.7)),
                    ('clf', LogisticRegression(**self.best_params))
                ])
                model.fit(X_tr, y_tr)
            cv_model.append(model)
            preds_tr = model.predict(X_tr)
            preds_val = model.predict(X_val)
            if self.metric == "f1":
                scores_val.append(metrics.f1_score(y_val, preds_val, average=AVG_METRIC))
                scores_tr.append(metrics.f1_score(y_tr, preds_tr, average=AVG_METRIC))
            else:
                scores_val.append(metrics.accuracy_score(y_val, preds_val))
                scores_tr.append(metrics.accuracy_score(y_tr, preds_tr))
            print(f"Fold {n + 1} - {self.metric}: train = {scores_tr[n]}, validation = {scores_val[n]}")
            n += 1
        return cv_model, np.mean(scores_tr), np.mean(scores_val)

    @staticmethod
    def predict(cv_model, X_data, clean_mode=None):
        """
        :description: predict text
        :param cv_model: pretrained model
        :param X_data: text data to classify
        :param clean_mode: cleansing pre-processing -'normal', 'stemma', 'lemma' or None-
        :return: predictions (:type: list)
        """
        if clean_mode:
            X = []
            for x in X_data:
                lang, _ = langid.classify(str(x))  # Detect language
                clean_txt = NlpUtils().clean_text(str(x), lang)  # Clean text with basic transformations
                if clean_mode == "stemma":  # Calculate stemmas
                    clean_txt = NlpUtils().stem_text(clean_txt, lang)
                if clean_mode == "lemma":  # Calculate lemmas
                    clean_txt = NlpUtils().lemma_text(clean_txt, lang)
                X.append(clean_txt)
        else:
            X = [str(x) for x in X_data]
        preds = []
        for model in cv_model:
            preds.append(model.predict(X))
        preds = np.array(preds).T.tolist()
        preds = [mode(p) for p in preds]
        return preds


class NNclf:
    def baseline(self, n_features, n_classes, dense_layers=4, neurons_by_layer=8, activation="tanh", dropout_rate=0.2,
                       optimizer="adam", loss="mean_squared_error", metric="f1"):
        # start model
        model = Sequential()
        # Input layer
        model.add(Dense(units=neurons_by_layer, input_dim=n_features, activation=activation))
        # creates a Dense model with the number of layers, neurons and dropout_rate specified
        for dl in range(dense_layers):
            model.add(Dense(units=neurons_by_layer, activation=activation))
        # add dropout layer to avoid overfitting.
        model.add(Dropout(dropout_rate))
        # add dense (outout) layer
        model.add(Dense(n_classes, activation='softmax'))
        # compile model
        if metric == "f1":
            metric = self.avg_f1
        else:
            metric = "accuracy"
        model.compile(optimizer=optimizer, loss=loss, metrics=[metric])
        return model

    @staticmethod
    def predict(model, X_data):
        pred = list(model.predict(X_data, verbose=False))
        return [model.classes_[np.argmax(p)] for p in pred]

    @staticmethod
    def avg_f1(y_true, y_pred):
        true_positives = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)))
        predicted_positives = backend.sum(backend.round(backend.clip(y_pred, 0, 1)))
        possible_positives = backend.sum(backend.round(backend.clip(y_true, 0, 1)))
        precision = true_positives / (predicted_positives + backend.epsilon())
        recall = true_positives / (possible_positives + backend.epsilon())
        return 2 * ((precision * recall) / (precision + recall + backend.epsilon()))
