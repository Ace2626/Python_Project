from collections import Counter

class cap_parser:
    def __init__(self, cap_text : str):
        self.text = cap_text
        self.pointer = 0
        self.current = self.text[self.pointer]

    def next(self):
        self.pointer += 1
        return self.text[self.pointer]

    def is_end(self):
        return self.text[self.pointer + 1 ] == None

def format_text_for_word_freq(text : str):
    chars = [',','.','?','!']
    for char in chars:
        text = text.replace(char,'')

    text = text.lower()
    return text

def get_word_freq(words : list, text : str):

    formated_text = format_text_for_word_freq(text).split()
    text_data = Counter(formated_text)
    freqs = []

    for word in words:
        if word in text_data.keys():
            freqs.append(100*text_data[word]/len(formated_text))
        else:
            freqs.append(0)

    zipper = zip(words,freqs)
    result = dict(zipper)
    return result

def get_char_freq(chars : list, text :str):
    text_data = Counter(text.lower())
    freqs = []

    for char in chars:
        if char in text_data.keys():
            freqs.append(100*text_data[char]/len(text))
        else:
            freqs.append(0)

    zipper = zip(chars,freqs)
    result = dict(zipper)
    return result

def get_capital_run_length(cap_text : str):
    
    parse_tool = cap_parser(cap_text)
    run_counts = []
    current_run = 0

    while True:
        try:  
            while parse_tool.current.isupper():
                current_run += 1
                try:
                    parse_tool.current = parse_tool.next()
                except IndexError:
                    break
            
            if current_run > 0:
                run_counts.append(current_run)
                current_run = 0

            parse_tool.current = parse_tool.next()
        except IndexError:
            break

    cap_results = {}
    cap_results['average'] = sum(run_counts)/len(run_counts)
    cap_results['longest'] = max(run_counts)
    cap_results['total'] = sum(run_counts)
    return cap_results

def parse_text_data(text : str):
    key_words = ['make','address','all','3d','our','over','remove','internet','order','mail','receive','will','people','report','addresses','free','business','email','you','credit','your','font','000','money','hp','hpl','george','650','lab','labs','telnet','857','data','415','85','technology','1999','parts','pm','direct','cs','meeting','original','project','re','edu','table','conference']
    key_chars = [';','(','[','!','$','#']

    word_analysis = get_word_freq(key_words,text)
    char_analysis = get_char_freq(key_chars,text)
    cap_analysis = get_capital_run_length(text)

    results = dict(word_analysis)
    results.update(char_analysis)
    results.update(cap_analysis)

    res = []
    res.append([*results.values()])

    return res

def parse_json(json_file : dict):
    return list([json_file.values()])
