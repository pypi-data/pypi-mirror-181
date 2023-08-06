from preprocess import UserSentence
from bird_detection import BirdDetection


class Get_Bird_Names:
    def merge_lists(self, list1, final_list):
        for i in list1:
            if type(i) != str:
                i = str(i)
            if i not in final_list:
                final_list.append(i)
        return final_list

    def consolidate_bird_list(self, list1, list2):
        total_list = []
        total_list = self.merge_lists(list1, total_list)
        total_list = self.merge_lists(list2, total_list)

        i = 0
        while i < len(total_list):
            for elem in total_list:
                if elem.find(total_list[i]) > - 1 and elem != total_list[i]:
                    total_list.remove(total_list[i])
                    continue
            i += 1

        return total_list

    def return_bird_name(self, sentence):
        if len(sentence)>0:
            sentence = UserSentence(sentence)
            bd_ = BirdDetection()
            # Check if the bird can be found in any list.
            return_bird_list = bd_.find_bird_from_list(sentence.preprocessed_text)

            # Run the model.
            bird_list_ner = bd_.run_model(sentence.preprocessed_text)

            return_bird_list = self.consolidate_bird_list(return_bird_list, bird_list_ner)

            return return_bird_list
        else:
            return "No text found."

    def __init__(self):
        pass

obj_ = Get_Bird_Names()
print(obj_.return_bird_name("Common tailorbird flew away."))