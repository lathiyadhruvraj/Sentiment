from flask import Flask, request, render_template
from sentiment import stream, clean_tweet, analyse_sentiment, score
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        topic = request.form['search']
        no_of_tweets = request.form['no_of_tweets']

        frame = stream(query=topic, num=int(no_of_tweets))

        final = pd.DataFrame(columns=['clean_tweets', 'sentiments', 'score'])
        final['clean_tweets'] = frame['Tweets'].apply(lambda x: clean_tweet(x))
        final['sentiments'] = final['clean_tweets'].apply(lambda x: analyse_sentiment(x))
        final['score'] = final['clean_tweets'].apply(lambda x: score(x))
        together = final[['clean_tweets', 'sentiments', 'score']]

        pos = final[final['sentiments'] == 'POSITIVE'].shape[0]
        neu = final[final['sentiments'] == 'NEUTRAL'].shape[0]
        neg = final[final['sentiments'] == 'NEGATIVE'].shape[0]

        return render_template("start.html", pos=pos, neu=neu, neg=neg,
                               name=topic, data=frame.to_html(), together=together.to_html())

    return render_template('start.html')


if __name__ == '__main__':
    app.run(debug=True)
