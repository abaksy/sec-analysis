from gensim import models

lda_model =  models.LdaMulticore.load('lda.model')

# print all topics
rep = lda_model.show_topics(num_topics = 20)
for line in rep:
    print(line)

'''
with open('lda.model', 'r') as topic_file:
    topics=lda_model.top_topics(corpus)
    topic_file.write('\n'.join('%s %s' %topic for topic in topics))



# print topic 28
model.print_topic(10, topn=20)

# another way
for i in range(0, model.num_topics-1):
    print(model.print_topic(i))

# and another way, only prints top words
for t in range(0, model.num_topics-1):
    print('topic {}: '.format(t) + ', '.join([v[1] for v in model.show_topic(t, 20)]))
'''