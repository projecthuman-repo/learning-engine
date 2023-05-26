from app.mcq_generation import MCQGenerator

MCQ_Generator = MCQGenerator(False)

context = '''The koala or, inaccurately, koala bear[a] (Phascolarctos cinereus), is an arboreal herbivorous marsupial native to Australia. It is the only extant representative of the family Phascolarctidae and its closest living relatives are the wombats, which are members of the family Vombatidae. The koala is found in coastal areas of the mainland's eastern and southern regions, inhabiting Queensland, New South Wales, Victoria, and South Australia. It is easily recognisable by its stout, tailless body and large head with round, fluffy ears and large, spoon-shaped nose. The koala has a body length of 60–85 cm (24–33 in) and weighs 4–15 kg (9–33 lb). Fur colour ranges from silver grey to chocolate brown. Koalas from the northern populations are typically smaller and lighter in colour than their counterparts further south. These populations possibly are separate subspecies, but this is disputed.'''

#Obtain the answers from the generation of the multiple choice questions.
questions = MCQ_Generator.generate_mcq_questions(context, 8)
#Obtain the sentence in which these answers appear in order to create the fill-in-the-blank.
context_splits = MCQ_Generator._split_context_according_to_desired_count(context, 8)
#Find the index at which the answer starts in the sentence in order to help with the fill in the blank generation (i.e removing the answer)
#from the sentence.
start_idx = []
i = 0
#This algorithm cannot find the start of the answer "60-85 cm" for the sentence "The koala has a body length of 60–85 cm (24–33 in) and weighs 4–15 kg (9–33 lb)."
#However, it should not be an issue if the pre-processing of the texts replace the special character "–" with "-". This could be a re-occuring issue.
for sentence, answer in zip(context_splits, questions):
    print(sentence)
    print(answer.answerText)
    start_idx.append(sentence.lower().find(answer.answerText.lower()))
    print(start_idx[i])
    i = i+1
    print("--------------")


