import snscrape.modules.twitter as api
import pandas as pd
import json
import tweeds.classes.query as query


def make_json(data, jsonFilePath):
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def printRes(tweet: api.Tweet):
    print(f"{tweet.id} {tweet.date} <{tweet.user.username}> {tweet.content} \n")


def toOBJ(tweet: api.Tweet) -> object:
    return {
        "id": tweet.id,
        "date": tweet.date.strftime('%Y/%m/%d'),
        "username": tweet.user.username,
        "content": tweet.content,
        "likes": tweet.likeCount,
        "retweet": tweet.retweetCount,
        "reply": tweet.replyCount,
        "user": {
            "username": tweet.user.username,
            "followers": tweet.user.followersCount,
            "displayName": tweet.user.displayname,
            "id": tweet.user.id
        },
        "url": tweet.url
    }


def search(q: query.Query) -> None:
    query = ""

    if q.search:
        query += f"{q.search} "
    if q.username:
        query += f"(from:{q.username}) "
    if q.until:
        query += f"until:{q.until} "
    if q.since:
        query += f"since:{q.since} "
    if q.minLikes:
        query += f"min_faves:{q.minLikes} "
    if q.minReplies:
        query += f" min_replies:{q.minReplies} "
    if q.minRetweets:
        query += f" min_retweets:{q.minRetweets} "
    if q.near:
        query += f"near:{q.near} "

    jsonObj = {}
    csvObj = []

    for i, tweet in enumerate(api.TwitterSearchScraper(query).get_items()):
        if q.limit:
            if i == q.limit:
                break
        jsonObj[tweet.id] = toOBJ(tweet)
        csvObj.append(
            [tweet.id, tweet.date, tweet.content, tweet.url,
             tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.sourceLabel[12:]]
        )
        if q.silent:
            if q.csv or q.json:
                pass
        else:
            printRes(tweet)

    if q.json:
        if q.json.find(".json") != -1:
            make_json(jsonObj, q.json)
            print("Output saved in JSON!")

    if q.csv:
        df = pd.DataFrame(
            csvObj, columns=["ID", "Date", "Tweet", "URL", "Likes", "Retweet", "Replies", "Source"])
        df.to_csv(q.csv)
        print("Output saved in CSV!")
