import pickle
import pandas as pd
import numpy as np
import argparse

def preprocessing(knowit):
    knowit["start"] = 0
    knowit["end"] = 0

    for index, row in knowit.iterrows():
        key = row["scene"]
        start = int(key[-9:-5])
        end = int(key[-4:])
        knowit["start"].iloc[index] = start
        knowit["end"].iloc[index] = end

    knowit = knowit.rename(
        columns = {
            "answer1" : "a0",
            "answer2" : "a1",
            "answer3" : "a2",
            "answer4" : "a3",
            "idxCorrect" : "answer_id",
            "scene" : "video_id"
        }
    )
    knowit["answer_id"] = knowit["answer_id"]-1
    knowit["qid"] = [i for i in range(knowit.shape[0])]
    knowit = knowit.drop(
        columns = ["kg_type", "reason"]
    )
    knowit = knowit.drop(columns=["subtitle"])
    return knowit

def get_subtitles(knowit):
    dico = {}
    for index, row in knowit.iterrows():
        key = row["scene"]
        start = int(key[-9:-5])
        end = int(key[-4:])
        value = {
            "text" : row["subtitle"],
            "start" : start,
            "end" : end
        }
        if key in dico :
            dico[key].append(value)
        else :
            dico[key] = [value]
    return dico         


def preprocess(input_path, output_path):
    knowit_train = pd.read_csv(input_path+"knowit_data_train.csv", header=0, sep="\t")
    knowit_val = pd.read_csv(input_path+"knowit_data_val.csv", header=0, sep="\t")
    knowit_test = pd.read_csv(input_path+"knowit_data_test.csv", header=0, sep="\t")

    train = preprocessing(knowit_train)
    val = preprocessing(knowit_val)
    test = preprocessing(knowit_test)

    train.to_csv(output_path+"train.csv", index=False)
    val.to_csv(output_path+"val.csv", index=False)
    test.to_csv(output_path+"test.csv", index=False)

    subtitles = {**get_subtitles(knowit_train), **get_subtitles(knowit_val), **get_subtitles(knowit_test)}
    pickle.dump(subtitles, open(output_path+"subtitles.pkl", 'wb'))
    print("done !")

parser = argparse.ArgumentParser("Zdar", add_help=False)
parser.add_argument(
    "--input_path",
      default = ""
)
parser.add_argument(
    "--output_path",
      default = ""
)

if __name__ == "__main__" :
    args = parser.parse_args()
    preprocess(args.input_path, args.output_path)