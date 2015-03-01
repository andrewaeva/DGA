__author__ = 'andrewa'
import datetime
import random

verbs = ['people', 'history', 'way', 'art', 'money', 'world', 'information', 'map', 'two', 'family', 'government',
         'health', 'system', 'computer', 'meat', 'year', 'thanks', 'music', 'person', 'reading', 'method', 'data',
         'food', 'understanding', 'theory', 'law', 'bird', 'literature', 'problem', 'software', 'control', 'knowledge',
         'power', 'ability', 'economics', 'love', 'internet', 'television', 'science', 'library', 'nature', 'fact',
         'product', 'idea', 'temperature', 'investment', 'area', 'society', 'activity', 'story', 'industry', 'media',
         'thing', 'oven', 'community', 'definition', 'safety', 'quality', 'development', 'language', 'management',
         'player', 'variety', 'video', 'week', 'security', 'country', 'exam', 'movie', 'organization', 'equipment',
         'physics', 'analysis', 'policy', 'series', 'thought', 'basis', 'boyfriend', 'direction', 'strategy',
         'technology', 'army', 'camera', 'freedom', 'paper', 'environment', 'child', 'instance', 'month', 'truth',
         'marketing', 'university', 'writing', 'article', 'department', 'difference', 'goal', 'news', 'audience',
         'fishing', 'growth', 'income', 'marriage', 'user', 'combination', 'failure', 'meaning', 'medicine',
         'philosophy', 'teacher', 'communication', 'relation', 'restaurant', 'satisfaction', 'sector', 'signature',
         'significance', 'song', 'tooth', 'town', 'vehicle', 'volume', 'wife', 'accident', 'airport', 'appointment',
         'arrival', 'assumption', 'baseball', 'chapter', 'committee', 'conversation', 'database', 'enthusiasm', 'error',
         'explanation', 'farmer', 'gate', 'girl', 'hall', 'historian', 'hospital', 'injury', 'instruction',
         'maintenance', 'manufacturer', 'meal', 'perception', 'pie', 'poem', 'presence', 'proposal', 'reception',
         'replacement', 'revolution', 'river', 'son', 'speech', 'tea', 'village', 'warning', 'winner', 'worker',
         'writer', 'assistance', 'breath', 'buyer', 'chest', 'chocolate', 'conclusion', 'contribution', 'cookie',
         'courage', 'dad', 'desk', 'drawer', 'establishment', 'examination', 'garbage', 'grocery', 'honey',
         'impression', 'improvement', 'independence', 'insect', 'inspection', 'inspector', 'king', 'ladder', 'menu',
         'penalty', 'piano', 'potato', 'profession', 'professor', 'quantity', 'reaction', 'requirement', 'salad',
         'sister', 'supermarket', 'tongue', 'weakness', 'wedding', 'affair', 'ambition', 'analyst', 'apple',
         'assignment', 'assistant', 'bathroom', 'bedroom', 'beer', 'birthday', 'celebration', 'championship', 'cheek',
         'client', 'consequence', 'departure', 'diamond', 'dirt', 'ear', 'fortune', 'friendship', 'funeral', 'gene',
         'girlfriend', 'hat', 'indication', 'intention', 'lady', 'midnight', 'negotiation', 'obligation', 'passenger',
         'pizza', 'platform', 'poet', 'pollution', 'recognition', 'reputation', 'shirt', 'sir', 'speaker', 'stranger',
         'surgery', 'sympathy', 'tale', 'throat', 'trainer', 'uncle', 'youth', 'time', 'work', 'film', 'water',
         'example', 'while', 'business', 'study', 'game', 'life', 'form', 'air', 'day', 'place', 'number', 'part',
         'field', 'fish', 'back', 'process', 'heat', 'hand', 'experience', 'job', 'book', 'end', 'point', 'type',
         'home', 'economy', 'value', 'body', 'market', 'guide', 'interest', 'state', 'radio', 'course', 'company',
         'price', 'size', 'card', 'list', 'mind', 'trade', 'line', 'care', 'group', 'risk', 'word', 'fat', 'force',
         'key', 'light', 'training', 'name', 'school', 'top', 'amount', 'level', 'order', 'practice', 'research',
         'sense', 'service', 'piece', 'web', 'boss', 'sport', 'fun', 'house', 'page', 'term', 'test', 'answer', 'sound',
         'focus', 'matter', 'kind', 'soil', 'board', 'oil', 'picture', 'access', 'garden', 'range', 'rate', 'reason',
         'future', 'site', 'demand', 'exercise', 'image', 'case', 'cause', 'coast', 'action', 'age', 'bad', 'boat',
         'record', 'result', 'section', 'building', 'mouse', 'cash', 'class', 'nothing', 'period', 'plan', 'store',
         'tax', 'side', 'subject', 'space', 'rule', 'stock', 'weather', 'chance', 'figure', 'man', 'model', 'source',
         'beginning', 'earth', 'program', 'chicken', 'design', 'feature', 'head', 'material', 'purpose', 'question',
         'rock', 'salt', 'act', 'birth', 'car', 'dog', 'object', 'scale', 'sun', 'note', 'profit', 'rent', 'speed',
         'style', 'war', 'bank', 'craft', 'half', 'inside', 'outside', 'standard', 'bus', 'exchange', 'eye', 'fire',
         'position', 'pressure', 'stress', 'advantage', 'benefit', 'box', 'frame', 'issue', 'step', 'cycle', 'face',
         'item', 'metal', 'paint', 'review', 'room', 'screen', 'structure', 'view', 'account', 'ball', 'discipline',
         'medium', 'share', 'balance', 'bit', 'black', 'bottom', 'choice', 'gift', 'impact', 'machine', 'shape', 'tool',
         'wind', 'address', 'average', 'career', 'culture', 'morning', 'pot', 'sign', 'table', 'task', 'condition',
         'contact', 'credit', 'egg', 'hope', 'ice', 'network', 'north', 'square', 'attempt', 'date', 'effect', 'link',
         'post', 'star', 'voice', 'capital', 'challenge', 'friend', 'self', 'shot', 'brush', 'couple', 'exit', 'front',
         'function', 'lack', 'living', 'plant', 'plastic', 'spot', 'summer', 'taste', 'theme', 'track', 'wing', 'brain',
         'button', 'click', 'desire', 'foot', 'gas', 'influence', 'mood', 'notice', 'rain', 'wall', 'base', 'damage',
         'distance', 'feeling', 'pair', 'saving', 'staff', 'sugar', 'target', 'text', 'animal', 'author', 'budget',
         'discount', 'file', 'ground', 'lesson', 'minute', 'officer', 'phase', 'reference', 'register', 'sky', 'stage',
         'stick', 'title', 'trouble', 'bowl', 'bridge', 'campaign', 'character', 'club', 'edge', 'evidence', 'fan',
         'letter', 'lock', 'maximum', 'novel', 'option', 'pack', 'park', 'plenty', 'quarter', 'skin', 'sort', 'weight',
         'baby', 'background', 'carry', 'dish', 'factor', 'fruit', 'glass', 'joint', 'master', 'muscle', 'red',
         'strength', 'traffic', 'trip', 'vegetable', 'appeal', 'chart', 'gear', 'ideal', 'kitchen', 'land', 'log',
         'mother', 'net', 'party', 'principle', 'relative', 'sale', 'season', 'signal', 'spirit', 'street', 'tree',
         'wave', 'belt', 'bench', 'commission', 'copy', 'drop', 'minimum', 'path', 'progress', 'project', 'sea',
         'south', 'status', 'stuff', 'ticket', 'tour', 'angle', 'blue', 'breakfast', 'confidence', 'daughter', 'degree',
         'doctor', 'dot', 'dream', 'duty', 'essay', 'father', 'fee', 'finance', 'hour', 'juice', 'luck', 'milk',
         'mouth', 'peace', 'pipe', 'stable', 'storm', 'substance', 'team', 'trick', 'afternoon', 'bat', 'beach',
         'blank', 'catch', 'chain', 'consideration', 'cream', 'crew', 'detail', 'gold', 'interview', 'kid', 'mark',
         'mission', 'pain', 'pleasure', 'score', 'screw', 'sex', 'shop', 'shower', 'suit', 'tone', 'window', 'agent',
         'band', 'bath', 'block', 'bone', 'calendar', 'candidate', 'cap', 'coat', 'contest', 'corner', 'court', 'cup',
         'district', 'door', 'east', 'finger', 'garage', 'guarantee', 'hole', 'hook', 'implement', 'layer', 'lecture',
         'lie', 'manner', 'meeting', 'nose', 'parking', 'partner', 'profile', 'rice', 'routine', 'schedule', 'swimming',
         'telephone', 'tip', 'winter', 'airline', 'bag', 'battle', 'bed', 'bill', 'bother', 'cake', 'code', 'curve',
         'designer', 'dimension', 'dress', 'ease', 'emergency', 'evening', 'extension', 'farm', 'fight', 'gap', 'grade',
         'holiday', 'horror', 'horse', 'host', 'husband', 'loan', 'mistake', 'mountain', 'nail', 'noise', 'occasion',
         'package', 'patient', 'pause', 'phrase', 'proof', 'race', 'relief', 'sand', 'sentence', 'shoulder', 'smoke',
         'stomach', 'string', 'tourist', 'towel', 'vacation', 'west', 'wheel', 'wine', 'arm', 'aside', 'associate',
         'bet', 'blow', 'border', 'branch', 'breast', 'brother', 'buddy', 'bunch', 'chip', 'coach', 'cross', 'document',
         'draft', 'dust', 'expert', 'floor', 'god', 'golf', 'habit', 'iron', 'judge', 'knife', 'landscape', 'league',
         'mail', 'mess', 'native', 'opening', 'parent', 'pattern', 'pin', 'pool', 'pound', 'request', 'salary', 'shame',
         'shelter', 'shoe', 'silver', 'tackle', 'tank', 'trust', 'assist', 'bake', 'bar', 'bell', 'bike', 'blame',
         'boy', 'brick', 'chair', 'closet', 'clue', 'collar', 'comment', 'conference', 'devil', 'diet', 'fear', 'fuel',
         'glove', 'jacket', 'lunch', 'monitor', 'mortgage', 'nurse', 'pace', 'panic', 'peak', 'plane', 'reward', 'row',
         'sandwich', 'shock', 'spite', 'spray', 'surprise', 'till', 'transition', 'weekend', 'welcome', 'yard', 'alarm',
         'bend', 'bicycle', 'bite', 'blind', 'bottle', 'cable', 'candle', 'clerk', 'cloud', 'concert', 'counter',
         'flower', 'grandfather', 'harm', 'knee', 'lawyer', 'leather', 'load', 'mirror', 'neck', 'pension', 'plate',
         'purple', 'ruin', 'ship', 'skirt', 'slice', 'snow', 'specialist', 'stroke', 'switch', 'trash', 'tune', 'zone',
         'anger', 'award', 'bid', 'bitter', 'boot', 'bug', 'camp', 'candy', 'carpet', 'cat', 'champion', 'channel',
         'clock', 'comfort', 'cow', 'crack', 'engineer', 'entrance', 'fault', 'grass', 'guy']
nouns = ['is', 'are', 'has', 'get', 'see', 'need', 'know', 'would', 'find', 'take', 'want', 'does', 'learn', 'become',
         'come', 'include', 'thank', 'provide', 'create', 'add', 'understand', 'consider', 'choose', 'develop',
         'remember', 'determine', 'grow', 'allow', 'supply', 'bring', 'improve', 'maintain', 'begin', 'exist', 'tend',
         'enjoy', 'perform', 'decide', 'identify', 'continue', 'protect', 'require', 'occur', 'write', 'approach',
         'avoid', 'prepare', 'build', 'achieve', 'believe', 'receive', 'seem', 'discuss', 'realize', 'contain',
         'follow', 'refer', 'solve', 'describe', 'prefer', 'prevent', 'discover', 'ensure', 'expect', 'invest',
         'reduce', 'speak', 'appear', 'explain', 'explore', 'involve', 'lose', 'afford', 'agree', 'hear', 'remain',
         'represent', 'apply', 'forget', 'recommend', 'rely', 'vary', 'generate', 'obtain', 'accept', 'communicate',
         'complain', 'depend', 'enter', 'happen', 'indicate', 'suggest', 'survive', 'appreciate', 'compare', 'imagine',
         'manage', 'differ', 'encourage', 'expand', 'prove', 'react', 'recognize', 'relax', 'replace', 'borrow', 'earn',
         'emphasize', 'enable', 'operate', 'reflect', 'send', 'anticipate', 'assume', 'engage', 'enhance', 'examine',
         'install', 'participate', 'intend', 'introduce', 'relate', 'settle', 'smell', 'assure', 'attract',
         'distribute', 'overcome', 'owe', 'succeed', 'suffer', 'throw', 'acquire', 'adapt', 'adjust', 'argue', 'arise',
         'confirm', 'encouraging', 'incorporate', 'justify', 'organize', 'ought', 'possess', 'relieve', 'retain',
         'shut', 'calculate', 'compete', 'consult', 'deliver', 'extend', 'investigate', 'negotiate', 'qualify',
         'retire', 'rid', 'weigh', 'arrive', 'attach', 'behave', 'celebrate', 'convince', 'disagree', 'establish',
         'ignore', 'imply', 'insist', 'pursue', 'remaining', 'specify', 'warn', 'accuse', 'admire', 'admit', 'adopt',
         'announce', 'apologize', 'approve', 'attend', 'belong', 'commit', 'criticize', 'deserve', 'destroy',
         'hesitate', 'illustrate', 'inform', 'manufacturing', 'persuade', 'pour', 'propose', 'remind', 'shall',
         'submit', 'suppose', 'translate', 'be', 'have', 'use', 'make', 'look', 'help', 'go', 'being', 'think', 'read',
         'keep', 'start', 'give', 'play', 'feel', 'put', 'set', 'change', 'say', 'cut', 'show', 'try', 'check', 'call',
         'move', 'pay', 'let', 'increase', 'turn', 'ask', 'buy', 'guard', 'hold', 'offer', 'travel', 'cook', 'dance',
         'excuse', 'live', 'purchase', 'deal', 'mean', 'fall', 'produce', 'search', 'spend', 'talk', 'upset', 'tell',
         'cost', 'drive', 'support', 'remove', 'return', 'run', 'appropriate', 'reserve', 'leave', 'reach', 'rest',
         'serve', 'watch', 'charge', 'break', 'stay', 'visit', 'affect', 'cover', 'report', 'rise', 'walk', 'pick',
         'lift', 'mix', 'stop', 'teach', 'concern', 'fly', 'born', 'gain', 'save', 'stand', 'fail', 'lead', 'listen',
         'worry', 'express', 'handle', 'meet', 'release', 'sell', 'finish', 'press', 'ride', 'spread', 'spring', 'wait',
         'display', 'flow', 'hit', 'shoot', 'touch', 'cancel', 'cry', 'dump', 'push', 'select', 'conflict', 'die',
         'eat', 'fill', 'jump', 'kick', 'pass', 'pitch', 'treat', 'abuse', 'beat', 'burn', 'deposit', 'print', 'raise',
         'sleep', 'advance', 'connect', 'consist', 'contribute', 'draw', 'fix', 'hire', 'join', 'kill', 'sit', 'tap',
         'win', 'attack', 'claim', 'drag', 'drink', 'guess', 'pull', 'wear', 'wonder', 'count', 'doubt', 'feed',
         'impress', 'repeat', 'seek', 'sing', 'slide', 'strip', 'wish', 'collect', 'combine', 'command', 'dig',
         'divide', 'hang', 'hunt', 'march', 'mention', 'survey', 'tie', 'escape', 'expose', 'gather', 'hate', 'repair',
         'scratch', 'strike', 'employ', 'hurt', 'laugh', 'lay', 'respond', 'split', 'strain', 'struggle', 'swim',
         'train', 'wash', 'waste', 'convert', 'crash', 'fold', 'grab', 'hide', 'miss', 'permit', 'quote', 'recover',
         'resolve', 'roll', 'sink', 'slip', 'suspect', 'swing', 'twist', 'concentrate', 'estimate', 'prompt', 'refuse',
         'regret', 'reveal', 'rush', 'shake', 'shift', 'shine', 'steal', 'suck', 'surround', 'bear', 'dare', 'delay',
         'hurry', 'invite', 'kiss', 'marry', 'pop', 'pray', 'pretend', 'punch', 'quit', 'reply', 'resist', 'rip', 'rub',
         'smile', 'spell', 'stretch', 'tear', 'wake', 'wrap', 'was', 'like', 'even', 'film', 'water', 'been', 'well',
         'were', 'example', 'own', 'study', 'must', 'form', 'air', 'place', 'number', 'part', 'field', 'fish',
         'process', 'heat', 'hand', 'experience', 'job', 'book', 'end', 'point', 'type', 'value', 'body', 'market',
         'guide', 'interest', 'state', 'radio', 'course', 'company', 'price', 'size', 'card', 'list', 'mind', 'trade',
         'line', 'care', 'group', 'risk', 'word', 'force', 'light', 'name', 'school', 'amount', 'order', 'practice',
         'research', 'sense', 'service', 'piece', 'web', 'boss', 'sport', 'page', 'term', 'test', 'answer', 'sound',
         'focus', 'matter', 'soil', 'board', 'oil', 'picture', 'access', 'garden', 'open', 'range', 'rate', 'reason',
         'according', 'site', 'demand', 'exercise', 'image', 'case', 'cause', 'coast', 'age', 'boat', 'record',
         'result', 'section', 'building', 'mouse', 'cash', 'class', 'dry', 'plan', 'store', 'tax', 'involved', 'side',
         'space', 'rule', 'weather', 'figure', 'man', 'model', 'source', 'earth', 'program', 'design', 'feature',
         'purpose', 'question', 'rock', 'act', 'birth', 'dog', 'object', 'scale', 'sun', 'fit', 'note', 'profit',
         'related', 'rent', 'speed', 'style', 'war', 'bank', 'content', 'craft', 'bus', 'exchange', 'eye', 'fire',
         'position', 'pressure', 'stress', 'advantage', 'benefit', 'box', 'complete', 'frame', 'issue', 'limited',
         'step', 'cycle', 'face', 'interested', 'metal', 'paint', 'review', 'room', 'screen', 'structure', 'view',
         'account', 'ball', 'concerned', 'discipline', 'ready', 'share', 'balance', 'bit', 'black', 'bottom', 'gift',
         'impact', 'machine', 'shape', 'tool', 'wind', 'address', 'average', 'career', 'culture', 'pot', 'sign',
         'table', 'task', 'condition', 'contact', 'credit', 'egg', 'hope', 'ice', 'network', 'separate', 'attempt',
         'date', 'effect', 'link', 'perfect', 'post', 'star', 'voice', 'challenge', 'friend', 'warm', 'brush', 'couple',
         'exit', 'experienced', 'function', 'lack', 'plant', 'spot', 'summer', 'taste', 'theme', 'track', 'wing',
         'brain', 'button', 'click', 'correct', 'desire', 'fixed', 'foot', 'gas', 'influence', 'notice', 'rain', 'wall',
         'base', 'damage', 'distance', 'pair', 'staff', 'sugar', 'target', 'text', 'author', 'complicated', 'discount',
         'file', 'ground', 'lesson', 'officer', 'phase', 'reference', 'register', 'secure', 'sky', 'stage', 'stick',
         'title', 'trouble', 'advanced', 'bowl', 'bridge', 'campaign', 'club', 'edge', 'evidence', 'fan', 'letter',
         'lock', 'option', 'organized', 'pack', 'park', 'quarter', 'skin', 'sort', 'weight', 'baby', 'carry', 'dish',
         'exact', 'factor', 'fruit', 'muscle', 'traffic', 'trip', 'appeal', 'chart', 'gear', 'land', 'log', 'lost',
         'net', 'season', 'spirit', 'tree', 'wave', 'belt', 'bench', 'closed', 'commission', 'copy', 'drop', 'firm',
         'frequent', 'progress', 'project', 'stuff', 'ticket', 'tour', 'angle', 'blue', 'breakfast', 'doctor', 'dot',
         'dream', 'essay', 'father', 'fee', 'finance', 'juice', 'luck', 'milk', 'mixed', 'mouth', 'pipe', 'please',
         'stable', 'storm', 'team', 'amazing', 'bat', 'beach', 'blank', 'busy', 'catch', 'chain', 'cream', 'crew',
         'detail', 'detailed', 'interview', 'kid', 'mark', 'pain', 'pleasure', 'score', 'screw', 'sex', 'sharp', 'shop',
         'shower', 'suit', 'tone', 'window', 'wise', 'band', 'bath', 'block', 'bone', 'calendar', 'candidate', 'cap',
         'coat', 'contest', 'court', 'cup', 'district', 'finger', 'garage', 'guarantee', 'hole', 'hook', 'implement',
         'layer', 'lecture', 'lie', 'married', 'narrow', 'nose', 'partner', 'profile', 'rice', 'schedule', 'telephone',
         'tip', 'bag', 'battle', 'bed', 'bill', 'bother', 'cake', 'code', 'curve', 'dimension', 'ease', 'farm', 'fight',
         'gap', 'grade', 'horse', 'host', 'husband', 'loan', 'mistake', 'nail', 'noise', 'occasion', 'package', 'pause',
         'phrase', 'race', 'sand', 'sentence', 'shoulder', 'smoke', 'stomach', 'string', 'surprised', 'towel',
         'vacation', 'wheel', 'arm', 'associate', 'bet', 'blow', 'border', 'branch', 'breast', 'buddy', 'bunch', 'chip',
         'coach', 'cross', 'document', 'draft', 'dust', 'floor', 'golf', 'habit', 'iron', 'judge', 'knife', 'landscape',
         'league', 'mail', 'mess', 'parent', 'pattern', 'pin', 'pool', 'pound', 'request', 'salary', 'shame', 'shelter',
         'shoe', 'tackle', 'tank', 'trust', 'assist', 'bake', 'bar', 'bell', 'bike', 'blame', 'brick', 'chair',
         'closet', 'clue', 'collar', 'comment', 'conference', 'devil', 'diet', 'fear', 'fuel', 'glove', 'jacket',
         'lunch', 'monitor', 'mortgage', 'nurse', 'pace', 'panic', 'peak', 'provided', 'reward', 'row', 'sandwich',
         'shock', 'spite', 'spray', 'surprise', 'till', 'transition', 'weekend', 'yard', 'alarm', 'bend', 'bicycle',
         'bite', 'blind', 'bottle', 'cable', 'candle', 'clerk', 'cloud', 'concert', 'counter', 'dirty', 'flower',
         'grandfather', 'harm', 'knee', 'lawyer', 'load', 'loose', 'mirror', 'neck', 'pension', 'plate', 'pleased',
         'proposed', 'ruin', 'ship', 'skirt', 'slice', 'snow', 'stroke', 'switch', 'tired', 'trash', 'tune', 'worried',
         'zone', 'anger', 'award', 'bid', 'boot', 'bug', 'camp', 'candy', 'carpet', 'cat', 'champion', 'channel',
         'clock', 'comfort', 'cow', 'crack', 'disappointed', 'empty', 'engineer', 'entrance', 'fault', 'grass', 'guy',
         'highlight', 'island', 'joke', 'jury', 'leg', 'lip', 'mate', 'nerve', 'passage', 'pen', 'pride', 'priest',
         'promise', 'resort', 'ring', 'roof', 'rope', 'sail', 'scheme', 'script', 'slight', 'smart', 'sock', 'station',
         'toe', 'tower', 'truck', 'witness']

domain_seed = 0xDEAD
next_domain = 1
const1 = 0xDEAD
const2 = 0xBEEF


def get_date():
    dt = str(datetime.datetime.now()).split(' ')[0]
    dstash = dt.split('-')
    dd = dstash[2]
    mm = dstash[1]
    yyyy = dstash[0]
    return int(dd), int(mm), int(yyyy)


def choose_word(word_list):
    global domain_seed
    global next_domain
    global const1
    global const2
    #time = get_date()[0]
    time = random.randint(1, 10000)
    domain_seed = (((((((((((domain_seed & 0xFFFF) * const1) & 0xFFFF) * time) & 0xFFFF) * const2) & 0xFFFF) *
                      next_domain) & 0xFFFF) ^ const1) & 0xFFFF)
    rem = domain_seed % len(word_list)
    next_domain += 1
    return word_list[rem]


def generate_domain():
    global nouns
    global verbs
    domain = ''
    start_flag = 0
    while len(domain) < 24:
        if start_flag == 0:
            domain += choose_word(verbs)
            start_flag = 1
        domain += choose_word(nouns)
    domain += '.com'
    return domain


for i in xrange(0, 100000):
    print generate_domain()
