from sklearn import linear_model, svm, tree, ensemble, naive_bayes, neighbors, feature_extraction as fe


SK_SUPPORTED_MODELS = (
    linear_model.SGDClassifier,
    linear_model.LogisticRegression,
    svm.SVC,
    tree.DecisionTreeClassifier,
    tree.ExtraTreeClassifier,
    ensemble.AdaBoostClassifier,
    ensemble.BaggingClassifier,
    ensemble.ExtraTreesClassifier,
    ensemble.GradientBoostingClassifier,
    ensemble.RandomForestClassifier,
    naive_bayes.BernoulliNB,
    naive_bayes.ComplementNB,
    naive_bayes.GaussianNB,
    naive_bayes.MultinomialNB,
    neighbors.KNeighborsClassifier,
)

SK_SUPPORTED_TOKENIZERS = (
    fe.text.CountVectorizer,
    fe.text.TfidfVectorizer,
    fe.text.HashingVectorizer,
)
