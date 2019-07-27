# DO NOT RUN THIS CODE AGAIN - AS FINAL MENTORS FILE HAS CHANGED
# import json
# import os
#
# # read all files from data folder, create new dict,
# # append every item to the dict
# # write to json
#
# filenames = os.walk("./data").__next__()[2]
# final_mentors = {}
# d_sum = 0
# s = set()
#
# for f in filenames:
#     if ".json" not in f:
#         continue
#     if 'final_mentors.json' in f:
#         continue
#     # if 'test_replies_mentor_data.json' in f:
#     #     continue
#     with open('./data/'+f, 'rb') as fname:
#         d = json.load(fname)
#         d_sum += len(d)
#         for k, v in d.items():
#             s.add(k)
#             # if v["screen_name"]=="gretchenatwood":
#             #     print('f', f)
#             final_mentors[k] = v
#
# with open('./data/final_mentors.json', 'w') as fname:
#     json.dump(final_mentors, fname, indent=4)
#
# with open('./data/final_mentors.json', 'rb') as fname:
#     d = json.load(fname)
#     print('final_mentor_file_sum', len(d))
#     print('Number of duplicates', d_sum - len(s))
#
# # all sum 2694
# # final_mentor_file_sum 1499
# # Number of duplicates 1195
#
#
#
# # To check if all keys in first file are present in the main big_file
#
# # with open('./data/final_mentors.json', 'rb') as fname:
# #     big_file = json.load(fname)
#
# # with open('./data/test_replies_mentor_data.json', 'rb') as fname:
# #     d = json.load(fname)
# #     for k, v in d.items():
# #         if k in big_file:
# #             print('k', k)
#
#
