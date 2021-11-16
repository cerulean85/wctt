from matplotlib import pyplot as plt


class ZHEvalPerformance:

    def get_binary_classification_measure(self,
                                          predicted_label_list,
                                          answer_label_list,
                                          threshold=0,
                                          label="Performance Result"):
        TP, FP, TN, FN = 0, 0, 0, 0
        for i in range(0, len(answer_label_list)):
            a = answer_label_list[i]
            p = predicted_label_list[i]

            if a == 1 and p == 1:
                TP += 1

            if a == 0 and p == 0:
                TN += 1

            if a == 1 and p == 0:
                FN += 1

            if a == 0 and p == 1:
                FP += 1

        b = (TP + FN)
        TPR = 0 if b == 0 else (TP / b)  # 민감도

        b = (TP + FP)
        PRECISION = 0 if b == 0 else (TP / b)

        b = (TN + FP)
        TNR = 0 if b == 0 else (TN / b)

        b = (TP + FP + FN + TN)
        ACCURACY = 0 if b == 0 else ((TP + TN) / b)
        ERROR_RATE = 0 if b == 0 else ((FP + FN) / b)

        b = PRECISION + TPR
        F1_SCORE = 2 * (0 if b == 0 else (PRECISION * TPR / b))

        result = {
            "TP": TP, "FP": FP, "TN": TN, "FN": FN,
            "TPR": TPR, "SENSITIVITY": TPR,
            "RECALL": TPR,
            "TNR": TNR, "SPECIFICITY": TNR, "1-SPECIFICITY": 1 - TNR, "FPR": 1 - TNR,
            "PRECISION": PRECISION,
            "F1-SCORE": F1_SCORE,
            "ACCURACY": ACCURACY,
            "ERROR_RATE": ERROR_RATE,
            "THRESHOLD": threshold
        }

        # print("========== {} ===============".format(label))
        # print("TP: {:.3f} , FP: {:.3f}, TN: {:.3f}, FN: {:.3f}".
        #       format(result["TP"], result["FP"], result["TN"], result["FN"]))
        # print("TPR: {:.3f} , FPR: {:.3f}, TNR: {:.3f}".
        #       format(result["TPR"], result["FPR"], result["TNR"]))
        # print("RECALL: {:.3f} , PRECISION: {:.3f}, ACCURACY: {:.3f}, F1-SCORE: {:.3f}".
        #       format(result["RECALL"], result["PRECISION"], result["ACCURACY"], result["F1-SCORE"]))
        # print("SPECIFICITY: {:.3f} , SPECIFICITY: {:.3f}, 1-SPECIFICITY: {:.3f}, ERROR_RATE: {:.3f}".
        #       format(result["SPECIFICITY"], result["SPECIFICITY"], result["1-SPECIFICITY"], result["ERROR_RATE"]))
        # print("THRESHOLD: {:.3f}".format(result["THRESHOLD"]))

        # for item in result.items():
            # name = item[0]
            # value = item[1] if type(item[1]) == "<class 'int'>" else
            # print("{}: {:.3f}".format(item[0], float(item[1])))
        # print("====================================")

        return result

    def get_roc_curve(self, specificity_list, sensitivity_list):
        plt.plot(specificity_list, sensitivity_list)
        plt.title('ROC Curve')
        plt.xlabel('1 - Specificity')
        plt.ylabel('Sensitivity')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()

    def get_auc(self, FPR, TPR):
        AUC_TPR = [0] + TPR
        AUC_FPR = [0] + FPR

        AUC = 0
        for i in range(1, len(AUC_TPR)):
            tmp_AUC = (AUC_TPR[i - 1] + AUC_TPR[i]) * (AUC_FPR[i] - AUC_FPR[i - 1]) / 2
            AUC += tmp_AUC

        return AUC

        # print(AUC)

        # fig = plt.figure()
        # fig.set_size_inches(15, 15)
        # plt.plot(FPR, TPR)
        # plt.fill_between(FPR, TPR, 0, facecolor="red", alpha=0.2)
        # plt.xlabel("FPR", fontsize=24)
        # plt.ylabel("TPR", fontsize=24)
        # plt.text(FPR[-1] / 2, TPR[-1] / 2, 'AUC : ' + str(AUC), fontsize=24)
        # plt.show()
