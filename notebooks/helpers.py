import itertools, time
from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score

def print_table(listx):
    for lists in listx:
        for i in lists:
            print("{0:<25}".format(i),end='\t')
        print()

        
def display_confusion_matrix(y_test, pred_test):
    """
    Displays a nice and pretty confusion matrix for our data set.
    """
    plt.figure()
    classes = ['Normal', 'Obfuscated']
    cm = confusion_matrix(y_test, pred_test)
    np.set_printoptions(precision=2)

    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

    
def evaluate_model(name, model, X_test, y_test):
    """
    Displays the Accuracy, F1, AUROC, and graphical confusion matrix for a mode.
    """
    pred_test = model.predict(X_test)
    pred_prob_test = [p[1] for p in model.predict_proba(X_test)]
    
    print(f"\n===== {name} =====\n")
    print("   Accuracy (test) :", "{:.4f}".format(accuracy_score(y_test, pred_test)))
    print("   F1       (test) :", "{:.4f}".format(f1_score(y_test, pred_test)))
    print("   AUROC    (test) :", "{:.4f}\n".format(roc_auc_score(y_test, pred_prob_test)))

    display_confusion_matrix(y_test, pred_test)


def train_model(model, X_train_data, y_train_data):
    
    start_time = time.time()
    model.fit(X_train_data, y_train_data)
    training_time = time.time() - start_time
    return(model, training_time)
