# usage: build zhihu dialog dataset
# author: WangYC@NWPU

import json
import jsonlines
import chardet
import re

# dst = '/data/wangyuanchun/chinese_data/zhihu/processed/parse/comments_all'
# dst = './comments_example'
# dst = './tmp'

question_file = './qa_example_100k'
answer_file = './answer_example_100k'
comments_file = './comments_example_100k'

qa_output_file = './output/qa_output_p.json'
one_hop_output_file = './output/one_hop_output_p.json'

show_dis_chi_num = False
adding_likct_condition = True
adding_dirty_filter = True
pure_chinese = True
chinese_ratio = 0.3

find_qa = True
find_qc = False
find_one_hop = True
find_two_hop = False

step = 1000

with open('./dirty_words.txt', 'r', encoding='utf-8') as f:
    dirty_words_list = f.read().splitlines()

def chi_num(tstr):
    tstr=tstr.replace(' ','')
    if len(tstr)==0:
        return False
    count=0
    for ch in tstr:
        if '\u4e00' <= ch <= '\u9fff':
            count+=1
    if count/len(tstr)<chinese_ratio:
        return False
    if count>2:
        return True
    return False

def dirty_filter(str_in):
    if pure_chinese:
        # weird_words_list = []
        for ch in str_in:
            # if '\u4e00' <= ch <= '\u9fff' or '\u0020' <= ch <= '\u007e':
            #     if 'a'<=ch<='z' or 'A'<=ch<='Z':
            #         str_in = str_in.replace(ch, '')
            #     else:
            #         continue

            if '\u4e00' <= ch <= '\u9fff' or '0' <= ch <= '9' or ch == ',' or ch == '。' or ch == '，' or ch == '!' or ch == '?' or ch == '！' or ch == '？':
                continue
            else:
                str_in = str_in.replace(ch, '')
        # if len(weird_words_list):
        #     print (weird_words_list)
        #     str_in = re.sub('|'.join(weird_words_list), '', str_in)
    return re.sub('|'.join(dirty_words_list), '', str_in)

if __name__ == '__main__':

    answer_set = set()
    question_set = set()
    comments_set = set()
    
    one_hop_set = set()
    qa_set = set()
    # qc_set = set()

    ite = 0

    all_questions = {}
    all_comments = {}
    all_answers = {}

    qa_list = []
    qc_list = []
    one_hop_list = []
    question_one_hot_list = []
    # two_hop_list = []

    question_structure = {}
    answer_structure = {}
    comment_structure = {}

    ts = {}
    # target_stucture = {
    #     "来源标识":" ",
    #     "主题":" ",
    #     "背景知识":" ",
    #     "对话历史":[" "," ", " "],
    #     "与Query相关的标准知识问答":[
    #         {"问题":" ", "上下文":" ", "答案":" "}
    #     ],
    #     "当前询问":" ",
    #     "后续对话":[" ", " "],
    #     "Y":" "
    # }

    #find all questions
    with open(question_file, encoding='utf-8') as file:
        question_ct = 0

        while True:
            line = file.readline()
            if not line:
                break
            try:
                js = json.loads(line)
            except:
                continue

            if ite % step == 0 : 
                print('scanning questions...this is ite: {}'.format(ite))

            try:
                question_content = js['content']
            except:
                ite = ite + 1
                continue

            if chi_num(question_content):
                # print(question_content)

                question_structure['content'] = question_content
                question_structure['tag'] = js['title']

                if adding_dirty_filter:
                    question_structure['content'] = dirty_filter(question_content)
                # question_structure['salt'] = js['_salt']

                # if adding_likct_condition and question_structure['salt'] == 0:
                #     question_structure = {}
                #     continue
                
                question_set.add(js['idstr'])
                all_questions[js['idstr']] = question_structure
                # print(question_structure)
                question_structure = {}

                question_ct = question_ct + 1
            else:
                if show_dis_chi_num:
                    print('id:{} is not chi_num'.format(js['idstr']))
            ite = ite + 1
        # print(all_questions)

    file.close()

    print('question scanning done. total iteration: {} and total question: {}'.format(ite, question_ct))
    ite = 0

    # js_str = json.dumps(all_questions, indent=4, ensure_ascii=False)
    # with open('question_output.json', 'w') as output:
    #     output.write(js_str)
    # output.close()
    
    # find all answers
    with open(answer_file, encoding='utf-8') as file:
        answer_ct = 0

        while True:
            if ite % step == 0 : 
                print('scanning answers...this is ite: {}'.format(ite))
            line = file.readline()
            if not line:
                break
            try:
                js = json.loads(line)
            except:
                continue

            try:
                answer_content = js['content']
            except:
                continue

            if chi_num(answer_content):
                # print(answer_content)

                answer_structure['pid_str'] = js['pid_str']
                answer_structure['content'] = answer_content
                if adding_dirty_filter:
                    answer_structure['content'] = dirty_filter(answer_content)
                answer_structure['salt'] = js['_salt']
                answer_structure['idstr'] = js['idstr']

                if adding_likct_condition and answer_structure['salt'] == 0:
                    answer_structure = {}
                    continue

                answer_set.add(js['idstr'])
                all_answers[js['idstr']] = answer_structure
                # print(answer_structure)
                answer_structure = {}

                answer_ct = answer_ct + 1
            else:
                if show_dis_chi_num:
                    print('id:{} is not chi_num'.format(js['idstr']))

            ite = ite + 1
        # print(all_answers)

    file.close()

    print('answer scanning done. total iteration: {} and total answer: {}'.format(ite, answer_ct))
    ite = 0

    # js_str = json.dumps(all_answers, indent=4, ensure_ascii=False)
    # with open('answer_output.json', 'w') as output:
    #     output.write(js_str)
    # output.close()

    # find all comments
    with open(comments_file, encoding='utf-8') as file:
        comments_ct = 0

        while True:
            if ite % step == 0 : 
                print('scanning comments...this is ite: {}'.format(ite))
            line = file.readline()
            if not line:
                break
            try:
                js = json.loads(line)
            except:
                continue

            try:
                comment_content = js['content']
            except:
                continue

            if chi_num(comment_content):

                comment_structure['content'] = comment_content
                if adding_dirty_filter:
                    comment_structure['content'] = dirty_filter(comment_content)                   
                comment_structure['likct'] = js['likct']
                comment_structure['pid_str'] = js['pid_str']
                comment_structure['idstr'] = js['idstr']

                if adding_likct_condition and comment_structure['likct'] == 0:
                    comment_structure = {}
                    continue

                comments_set.add(js['idstr'])
                all_comments[js['idstr']] = comment_structure
                # print(answer_structure)

                comment_structure = {}
                # if js['pid_str'] in s:
                #     print(js['idstr'] + ' and this is iteration {}'.format(ite))
                # if js['pid'] == '145375627':
                comments_ct = comments_ct + 1
            else:
                if show_dis_chi_num:
                    print('id:{} is not chi_num'.format(js['idstr']))

            ite = ite + 1
        # print(all_answers)
    file.close()

    print('comments scanning done. total iteration: {} and total comments: {}'.format(ite, comments_ct))
    ite = 0

    # with open('comments_output.json', 'w') as output:
    #     output.write(js_str)
    # output.close()

    #find question & answer
    if find_qa:
        qa_ct = 0
        for answer_str in answer_set:
            if ite % step == 0:
                print('finding qa...this is ite: {}'.format(ite))
            if all_answers[answer_str]['pid_str'] in question_set and chi_num(all_answers[answer_str]['content']):
                qa_set.add(answer_str)

                ts['来源标识'] = '知乎'
                ts['主题'] = ''
                ts['背景知识'] = ''
                ts['对话历史'] = ''
                ts['与Query相关的标准知识问答'] = [{'问题':'', '上下文':'', '答案':''}]
                ts['当前询问'] = all_questions[all_answers[answer_str]['pid_str']]['content']
                ts['后续对话'] = ''
                ts['Y'] = all_answers[answer_str]['content']

                if all_questions[all_answers[answer_str]['pid_str']]['tag'] != '':
                    ts['背景知识'] = all_questions[all_answers[answer_str]['pid_str']]['tag']

                if adding_likct_condition and all_answers[answer_str]['salt'] == 0:
                # comment_structure = {}
                    ts = {}
                    continue

                qa_list.append(ts)
                ts = {}
                qa_ct = qa_ct + 1
            ite = ite + 1

        print('qa finding done. total iteration: {} and total qa: {}'.format(ite, qa_ct))
        ite = 0

        with open(qa_output_file, 'a') as output:
            for qa in qa_list:
                js_str = json.dumps(qa, indent=4, ensure_ascii=False)
                output.write(js_str + '\n')
    
    if find_qc:
        qc_ct = 0
        for comment_str in comments_set:
            if ite % step == 0:
                print('finding qc...this is ite: {}'.format(ite))
            if all_comments[comment_str]['pid_str'] in question_set and chi_num(all_comments[comment_str]['content']):
                # qc_set.add(comment_str)

                ts['来源标识'] = '知乎'
                ts['主题'] = ''
                ts['背景知识'] = ''
                ts['对话历史'] = ''
                ts['与Query相关的标准知识问答'] = [{'问题':'', '上下文':'', '答案':''}]
                ts['当前询问'] = all_questions[all_comments[comment_str]['pid_str']]['content']
                ts['后续对话'] = ''
                ts['Y'] = all_comments[comment_str]['content']

                if adding_likct_condition and all_comments[comment_str]['likct'] == 0:
                # comment_structure = {}
                    ts = {}
                    continue

                qc_list.append(ts)
                ts = {}
                qc_ct = qc_ct + 1
            ite = ite + 1

        print('qc finding done. total iteration: {} and total qc: {}'.format(ite, qc_ct))
        ite = 0

        with open('qc_output.json', 'a') as output:
            for qc in qc_list:
                js_str = json.dumps(qc, indent=4, ensure_ascii=False)
                output.write(js_str + '\n')

    if find_one_hop:
        one_hop_ct = 0
        for comment_str in comments_set:
            if ite % step == 0:
                print('scanning one_hop_comments...this is ite: {}'.format(ite))
            if all_comments[comment_str]['pid_str'] in answer_set and chi_num(all_comments[comment_str]['content']):
                one_hop_set.add(comment_str)

                ts['来源标识'] = '知乎'
                ts['主题'] = ''
                ts['背景知识'] = ''
                ts['对话历史'] = ''
                ts['与Query相关的标准知识问答'] = [{'问题':'', '上下文':'', '答案':''}]
                ts['当前询问'] = all_answers[all_comments[comment_str]['pid_str']]['content']
                ts['后续对话'] = ''
                ts['Y'] = all_comments[comment_str]['content']

                if all_answers[all_comments[comment_str]['pid_str']]['idstr'] in qa_set:
                    ts['背景知识'] = all_questions[all_answers[all_comments[comment_str]['pid_str']]['pid_str']]
                    question_one_hot_list.append(all_comments[comment_str]['content'])

                if adding_likct_condition and all_comments[comment_str]['likct'] == 0:
                    # comment_structure = {}
                    ts = {}
                    continue

                one_hop_list.append(ts)
                ts = {}

                one_hop_ct = one_hop_ct + 1
            ite = ite + 1

        print('one_hop scanning done. total iteration: {} and total one_hop: {}'.format(ite, one_hop_ct))
        ite = 0

        # js_str = json.dumps(one_hop_dir, indent=4, ensure_ascii=False)
        # with open('one_hop_output.json', 'w') as output:
        #     output.write(js_str)

        with open(one_hop_output_file, 'a') as output:
            for one_hop in one_hop_list:
                js_str = json.dumps(one_hop, indent=4, ensure_ascii=False)
                output.write(js_str + '\n')

    if find_two_hop:
        two_hop_ct = 0
        for key, each_comment in all_comments.items():
            if ite % 100 == 0:
                print('scanning two_hop_comments...this is ite: {}'.format(ite))
            if each_comment['pid_str'] in comments_set and chi_num(each_comment['content']):
            
                two_hop_set.add(each_comment['idstr'])
                comment_structure['idstr'] = each_comment['idstr']
                comment_structure['content'] = each_comment['content']
                comment_structure['likct'] = each_comment['likct']
                comment_structure['pid_str'] = each_comment['pid_str']
                comment_structure['p_comment'] = all_comments[each_comment['pid_str']]['content']

                # ts['来源标识'] = 'zhihu'
                # ts['主题'] = ''
                # ts['背景知识'] = ''
                # ts['对话历史'] = ''
                # ts['与Query相关的标准知识问答'] = [{'问题':'', '上下文':'', '答案':''}]
                # ts['当前询问'] = all_comments[each_comment['pid_str']]['content']
                # ts['后续对话'] = ''
                # ts['Y'] = each_comment['content']

                if each_comment['pid_str'] in one_hop_set:
                    comment_structure['p_background'] = all_answers[all_comments[each_comment['pid_str']]['pid_str']]['content']
                    # ts['背景知识'] = all_answers[all_comments[each_comment['pid_str']]['pid_str']]['content']
                else:
                    comment_structure['p_background'] = ' '

                if adding_likct_condition and comment_structure['likct'] == 0:
                    comment_structure = {}
                    # ts = {}
                    continue

                two_hop_dir[each_comment['idstr']] = comment_structure

                comment_structure = {}
                # ts = {}

                two_hop_ct = two_hop_ct + 1
            ite = ite + 1

        print('two_hop scanning done. total iteration: {} and total two_hop: {}'.format(ite, two_hop_ct))

        js_str = json.dumps(two_hop_dir, indent=4, ensure_ascii=False)
        with open('two_hop_output.json', 'w') as output:
            output.write(js_str)

    with open('pair_list.txt', 'w') as file:
        for each in question_one_hot_list:
            file.write(each + '\n')

    
    # three_hop_ct = 0
    # for each_comment in two_hop_set:
    #     if ite % 100 == 0:
    #         print('scanning answers...this is ite: {}'.format(ite))
    #     if each_comment['pid_str'] in two_hop_set and chi_num(each_comment['content']):
    #         three_hop_set.add(each_comment['idstr'])
    #         three_hop_ct = three_hop_ct + 1

    #     ite = ite + 1
    # print('three_hop scanning done. total iteration: {} and total three_hop: {}'.format(ite, two_hop_ct))
    # ite = 0
        
    # for each in three_hop_set:
    #     with jsonlines.open(output_file, 'w', encoding='utf-8') as output_file:
    #         target_stucture['当前询问'] = all_comments[each['pid_str']]['content']
    #         target_stucture['Y'] = all_comments[each['idstr']]['content']
    #         output_file.write(target_structure)
    
    # print('done :-)')
        
                


