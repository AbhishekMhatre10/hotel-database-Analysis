# Correct way to import Tkinter
from tkinter import *
import tkinter as tk  # Import the Tkinter module as 'tk'
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk,Image
from pymongo import MongoClient
from tkinter import Tk, Label, Button, Toplevel, OptionMenu, StringVar, Text, Scrollbar, END, INSERT
from datetime import datetime, tzinfo, timezone
from tkinter import ttk

 

# Create an instance of Tkinter's Tk class
root = tk.Tk()  # Use 'tk.' prefix to refer to Tkinter classes and methods
root.title("HOTEL REVIEWS")
root.geometry("600x600")
# Example: Adding a label to the window
label = tk.Label(root, text="Query1: To Find How Many good bad and average reviews!!")
label.pack()

#### for query 4###
client = MongoClient('mongodb://localhost:27017/')
db = client['hoteldb']
collection = db['reviews']
############
def get_unique_provinces():
    unique_provinces = collection.distinct("province")
    return unique_provinces

def get_hotel_with_max_reviews(selected_province, selected_month):
    pipeline = [
        {"$unwind": "$reviews"},
        {
            "$project": {
                "_id": 0,
                "name": "$name",
                "city": "$city",
                "province": "$province",
                "sentiment": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {
                                    "$regexMatch": {
                                        "input": {
                                            "$concat": [
                                                "$reviews.text",
                                                " ",
                                                "$reviews.title"
                                            ]
                                        },
                                        "regex": "(excellent|awesome|fantastic|amazing|outstanding|superb|terrific|pleasing|positive|perfect|great|wonderful|impressive|superior|exceptional|satisfying|delightful|splendid|stellar|commendable|first-rate|pleasurable|exquisite|admirable|noteworthy|brilliant|charming|enjoyable|marvelous|positive|pleasant|immaculate|gratifying|uplifting|heartwarming|affirmative|captivating|favorable|constructive|exuberant|good service|excellent service|attentive service|friendly staff|helpful staff|courteous staff|prompt service|efficient service|professional service|polite staff|fast service|positive experience|positive stay|positive impression|positive feedback|positive vibes|excellent room|awesome amenities|fantastic service|amazing location|outstanding staff|superb facilities|terrific experience|pleasing ambiance|positive atmosphere|perfect stay|great hospitality|wonderful view|impressive decor|superior cleanliness|exceptional quality|satisfying comfort|delightful surroundings|splendid decor|stellar service|commendable staff|first-rate amenities|pleasurable stay|exquisite design|admirable features|noteworthy comfort|brilliant arrangement|charming atmosphere|enjoyable environment|marvelous setting)",
                                        "options": "i"
                                    }
                                },
                                "then": "positive"
                            }
                        ],
                        "default": "unknown"
                    }
                },
                "reviewMonth": {"$month": "$reviews.date"}
            }
        },
        {"$match": {"province": selected_province, "sentiment": "positive"}},
        {
            "$group": {
                "_id": {
                    "province": "$province",
                    "city": "$city",
                    "hotel": "$name",
                    "reviewMonth": "$reviewMonth"
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": {
                    "province": "$_id.province",
                    "city": "$_id.city",
                    "hotel": "$_id.hotel"
                },
                "reviews": {
                    "$push": {
                        "month": "$_id.reviewMonth",
                        "count": "$count"
                    }
                },
                "totalReviews": {"$sum": "$count"}
            }
        },
        {"$sort": {"totalReviews": -1}},
        {
            "$project": {
                "_id": 0,
                "province": "$_id.province",
                "city": "$_id.city",
                "hotel": "$_id.hotel",
                "reviews": "$reviews",
                "totalReviews": 1
            }
        }
    ]

    result = list(collection.aggregate(pipeline))
    return result

def on_search():
    selected_province = province_var2.get()
    selected_month = int(month_var.get())

    selected_hotels = get_hotel_with_max_reviews(selected_province, selected_month)

    if selected_hotels:
        display_result(selected_hotels)
    else:
        result_label.config(text="No data found")

def display_result(selected_hotels):
    # Display the bar graph
    plot_bar_graph(selected_hotels[:5])

def plot_bar_graph(selected_hotels):
    hotel_names = [hotel['hotel'] for hotel in selected_hotels]
    counts = [sum(review['count'] for review in hotel['reviews']) for hotel in selected_hotels]

    plt.bar(hotel_names, counts)
    plt.xlabel('Hotel')
    plt.ylabel('Positive Reviews Count')
    plt.title('Top 5 Hotels with Positive Reviews')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Show the bar graph
    plt.show()

#############
def fetch_and_display_data(selected_province):
    mongo_uri = 'mongodb://localhost:27017/'
    database_name = 'hoteldb'
    collection_name = 'reviews '
    pipeline = [
    {
        "$unwind": "$reviews"
    },
    {
        "$project": {
            "_id": 0,
            "name": "$name",
            "city": "$city",
            "province": "$province",
            "sentiment": {
                "$switch": {
                    "branches": [
                        {
                            "case": {
                                "$regexMatch": {
                                    "input": {
                                        "$concat": [
                                            "$reviews.text",
                                            " ",
                                            "$reviews.title",
                                        ]
                                    },
                                    "regex": "(excellent|awesome|fantastic|amazing|outstanding|superb|terrific|pleasing|positive|perfect|great|wonderful|impressive|superior|exceptional|satisfying|delightful|splendid|stellar|commendable|first-rate|pleasurable|exquisite|admirable|noteworthy|brilliant|charming|enjoyable|marvelous|positive|pleasant|immaculate|gratifying|uplifting|heartwarming|affirmative|captivating|favorable|constructive|exuberant|good service|excellent service|attentive service|friendly staff|helpful staff|courteous staff|prompt service|efficient service|professional service|polite staff|fast service|positive experience|positive stay|positive impression|positive feedback|positive vibes|excellent room|awesome amenities|fantastic service|amazing location|outstanding staff|superb facilities|terrific experience|pleasing ambiance|positive atmosphere|perfect stay|great hospitality|wonderful view|impressive decor|superior cleanliness|exceptional quality|satisfying comfort|delightful surroundings|splendid decor|stellar service|commendable staff|first-rate amenities|pleasurable stay|exquisite design|admirable features|noteworthy comfort|brilliant arrangement|charming atmosphere|enjoyable environment|marvelous setting)",
                                    "options": "i",
                                },
                            },
                            "then": "positive",
                        },
                        {
                            "case": {
                                "$regexMatch": {
                                    "input": {
                                        "$concat": [
                                            "$reviews.text",
                                            " ",
                                            "$reviews.title",
                                        ]
                                    },
                                    "regex": "(poor|terrible|awful|horrible|disappointing|unpleasant|dreadful|inferior|negative|displeasing|unsatisfactory|disastrous|atrocious|appalling|lousy|mediocre|subpar|pitiful|regrettable|unfavorable|unpleasant|dismal|dreadful|discouraging|lamentable|gloomy|unfortunate|repugnant|offensive|disgusting|vile|abysmal|dreary|deplorable|disheartening|oppressive|woeful|unpleasant|objectionable|inferior|repulsive|poor service|bad service|inattentive service|unfriendly staff|unhelpful staff|rude staff|slow service|inefficient service|unprofessional service|discourteous staff|negative experience|negative stay|negative impression|negative feedback|negative vibes|poor room|terrible amenities|awful service|horrible location|disappointing staff|unpleasant facilities|dreadful experience|inferior ambiance|negative atmosphere|displeasing stay|unsatisfactory decor|disastrous cleanliness|atrocious surroundings|appalling decor|lousy service|mediocre amenities|subpar view|pitiful hospitality|regrettable features|unfavorable comfort|unpleasant surroundings|dismal arrangement|dreadful environment|discouraging setting|lamentable design|gloomy atmosphere|unfortunate features|repugnant hospitality|offensive staff|disgusting service|vile ambiance|abysmal environment|dreary setting|deplorable cleanliness|disheartening decor|oppressive surroundings|woeful facilities|unpleasant room|objectionable amenities|inferior features|repulsive comfort|poor service|bad service|inattentive service|unfriendly staff|unhelpful staff|rude staff|slow service|inefficient service|unprofessional service|discourteous staff|negative experience|negative stay|negative impression|negative feedback|negative vibes|poor room|terrible amenities|awful service|horrible location|disappointing staff|unpleasant facilities|dreadful experience|inferior ambiance|negative atmosphere|displeasing stay|unsatisfactory decor|disastrous cleanliness|atrocious surroundings|appalling decor|lousy service|mediocre amenities|subpar view|pitiful hospitality|regrettable features|unfavorable comfort|unpleasant surroundings|dismal arrangement|dreadful environment|discouraging setting|lamentable design|gloomy atmosphere|unfortunate features|repugnant hospitality|offensive staff|disgusting service|vile ambiance|abysmal environment|dreary setting|deplorable cleanliness|disheartening decor|oppressive surroundings|woeful facilities|unpleasant room|objectionable amenities|inferior features|repulsive comfort)",
                                    "options": "i",
                                },
                            },
                            "then": "negative",
                        },
                        {
                            "case": {
                                "$regexMatch": {
                                    "input": {
                                        "$concat": [
                                            "$reviews.text",
                                            " ",
                                            "$reviews.title",
                                        ]
                                    },
                                    "regex": "(average|mediocre|ordinary|standard|typical|neutral|middling|so-so|common|routine|regular|adequate|fair|tolerable|passable|acceptable|moderate)",
                                    "options": "i",
                                },
                            },
                            "then": "average",
                        },
                    ],
                    "default": "unknown",
                },
            },
        }
    },
    {
        "$match": {
            "sentiment": {"$in": ["positive", "negative", "average"]}
        }
    },
    {
        "$group": {
            "_id": {
                "province": "$province",
                "city": "$city",
                "hotel": "$name",
                "sentiment": "$sentiment"
            },
            "count": {"$sum": 1}
        }
    },
    {
        "$group": {
            "_id": {
                "province": "$_id.province",
                "city": "$_id.city",
                "hotel": "$_id.hotel"
            },
            "sentiments": {
                "$push": {
                    "sentiment": "$_id.sentiment",
                    "count": "$count"
                }
            },
            "totalReviews": {"$sum": "$count"}
        }
    },
    {
        "$sort": {"totalReviews": -1}
    },
    {
        "$project": {
            "_id": 0,
            "province": "$_id.province",
            "city": "$_id.city",
            "hotel": "$_id.hotel",
            "reviews": "$sentiments",
            "totalReviews": 1
        }
    }
]
    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    # Add an additional match stage for the selected province
    match_stage = {"$match": {"province": selected_province}}
    pipeline_with_province = pipeline.copy()
    pipeline_with_province.insert(1, match_stage)

    # Execute the modified MongoDB aggregation pipeline
    result = client[database_name][collection_name].aggregate(pipeline_with_province)

    # Create a new window for displaying data
    data_window = Toplevel(root)
    data_window.title("List of Hotels and their reviews")
    data_window.geometry("800x600")  # Set the window size

    # Create a text widget to display the results in the new window
    text_info = Text(data_window, height=60, width=100, wrap="word")
    text_info.pack()

    # Create a scrollbar for the text widget in the new window
    scrollbar_info = Scrollbar(data_window)
    scrollbar_info.pack(side="right", fill="y")

    # Configure the scrollbar with the text widget in the new window
    text_info.config(yscrollcommand=scrollbar_info.set)

    # Insert data into the text widget in the new window
    for entry in result:
        text_info.insert(INSERT, f"Hotel: {entry['hotel']}, City: {entry['city']}, Province: {entry['province']}\n")
        text_info.insert(INSERT, f"Total Reviews: {entry['totalReviews']}\n")
        for review in entry['reviews']:
            text_info.insert(INSERT, f"{review['sentiment']}, Count: {review['count']}\n")

def graph2(xyear):

    print("_________YEAR:",xyear)
    client = MongoClient('mongodb://localhost:27017/')

    # Execute the MongoDB aggregation pipeline
    your_aggregation_pipeline = [
    {
        "$match": {
            "reviews.date": {"$exists": True, "$gte": datetime(2011, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                            "$lt": datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)}
        }
    },
    {
        "$project": {
            "_id": 0,
            "hotelId": "$_id",
            "month": {"$month": "$reviews.date"},
            "year": {"$year": "$reviews.date"},
            "sentiment": {
                "$switch": {
                    "branches": [
                        {
                            "case": {
                                "$regexMatch": {
                                    "input": {
                                        "$concat": [
                                            "$reviews.text",
                                            " ",
                                            "$reviews.title",
                                        ]
                                    },
                                    "regex": "(excellent|awesome|fantastic|amazing|outstanding|superb|terrific|pleasing|positive|perfect|great|wonderful|impressive|superior|exceptional|satisfying|delightful|splendid|stellar|commendable|first-rate|pleasurable|exquisite|admirable|noteworthy|brilliant|charming|enjoyable|marvelous|positive|pleasant|immaculate|gratifying|uplifting|heartwarming|affirmative|captivating|favorable|constructive|exuberant|good service|excellent service|attentive service|friendly staff|helpful staff|courteous staff|prompt service|efficient service|professional service|polite staff|fast service|positive experience|positive stay|positive impression|positive feedback|positive vibes|excellent room|awesome amenities|fantastic service|amazing location|outstanding staff|superb facilities|terrific experience|pleasing ambiance|positive atmosphere|perfect stay|great hospitality|wonderful view|impressive decor|superior cleanliness|exceptional quality|satisfying comfort|delightful surroundings|splendid decor|stellar service|commendable staff|first-rate amenities|pleasurable stay|exquisite design|admirable features|noteworthy comfort|brilliant arrangement|charming atmosphere|enjoyable environment|marvelous setting)",
                                    "options": "i",
                                },
                            },
                            "then": "positive",
                        },
                        {
                            "case": {
                                "$regexMatch": {
                                    "input": {
                                        "$concat": [
                                            "$reviews.text",
                                            " ",
                                            "$reviews.title",
                                        ]
                                    },
                                    "regex": "(poor|terrible|awful|horrible|disappointing|unpleasant|dreadful|inferior|negative|displeasing|unsatisfactory|disastrous|atrocious|appalling|lousy|mediocre|subpar|pitiful|regrettable|unfavorable|unpleasant|dismal|dreadful|discouraging|lamentable|gloomy|unfortunate|repugnant|offensive|disgusting|vile|abysmal|dreary|deplorable|disheartening|oppressive|woeful|unpleasant|objectionable|inferior|repulsive|poor service|bad service|inattentive service|unfriendly staff|unhelpful staff|rude staff|slow service|inefficient service|unprofessional service|discourteous staff|negative experience|negative stay|negative impression|negative feedback|negative vibes|poor room|terrible amenities|awful service|horrible location|disappointing staff|unpleasant facilities|dreadful experience|inferior ambiance|negative atmosphere|displeasing stay|unsatisfactory decor|disastrous cleanliness|atrocious surroundings|appalling decor|lousy service|mediocre amenities|subpar view|pitiful hospitality|regrettable features|unfavorable comfort|unpleasant surroundings|dismal arrangement|dreadful environment|discouraging setting|lamentable design|gloomy atmosphere|unfortunate features|repugnant hospitality|offensive staff|disgusting service|vile ambiance|abysmal environment|dreary setting|deplorable cleanliness|disheartening decor|oppressive surroundings|woeful facilities|unpleasant room|objectionable amenities|inferior features|repulsive comfort|poor service|bad service|inattentive service|unfriendly staff|unhelpful staff|rude staff|slow service|inefficient service|unprofessional service|discourteous staff|negative experience|negative stay|negative impression|negative feedback|negative vibes|poor room|terrible amenities|awful service|horrible location|disappointing staff|unpleasant facilities|dreadful experience|inferior ambiance|negative atmosphere|displeasing stay|unsatisfactory decor|disastrous cleanliness|atrocious surroundings|appalling decor|lousy service|mediocre amenities|subpar view|pitiful hospitality|regrettable features|unfavorable comfort|unpleasant surroundings|dismal arrangement|dreadful environment|discouraging setting|lamentable design|gloomy atmosphere|unfortunate features|repugnant hospitality|offensive staff|disgusting service|vile ambiance|abysmal environment|dreary setting|deplorable cleanliness|disheartening decor|oppressive surroundings|woeful facilities|unpleasant room|objectionable amenities|inferior features|repulsive comfort)",
                                    "options": "i",
                                },
                            },
                            "then": "negative",
                        },
                        {
                            "case": {
                                "$regexMatch": {
                                    "input": {
                                        "$concat": [
                                            "$reviews.text",
                                            " ",
                                            "$reviews.title",
                                        ]
                                    },
                                    "regex": "(average|mediocre|ordinary|standard|typical|neutral|middling|so-so|common|routine|regular|adequate|fair|tolerable|passable|acceptable|moderate)",
                                    "options": "i",
                                },
                            },
                            "then": "average",
                        },
                    ],
                    "default": "unknown",
                },
            },
        }
    },
    {
        "$match": {
            "sentiment": {"$in": ["positive", "negative"]}
        }
    },
    {
        "$group": {
            "_id": {
                "year": "$year",
                "month": "$month",
                "sentiment": "$sentiment"
            },
            "count": {"$sum": 1}
        }
    },
    {
        "$group": {
            "_id": {
                "year": "$_id.year",
                "month": "$_id.month"
            },
            "positive": {
                "$sum": {"$cond": {"if": {"$eq": ["$_id.sentiment", "positive"]}, "then": "$count", "else": 0}}
            },
            "negative": {
                "$sum": {"$cond": {"if": {"$eq": ["$_id.sentiment", "negative"]}, "then": "$count", "else": 0}}
            },
            "total": {"$sum": "$count"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "year": "$_id.year",
            "month": "$_id.month",
            "positive": 1,
            "negative": 1,
            "total": 1
        }
    },
    {
        "$sort": {
            "year": 1,
            "total": -1
        }
    },
    {
        "$group": {
            "_id": "$year",
            "data": {
                "$push": {
                    "year": "$year",
                    "month": "$month",
                    "monthName": {
                        "$switch": {
                            "branches": [
                                {"case": {"$eq": ["$month", 1]}, "then": "January"},
                                {"case": {"$eq": ["$month", 2]}, "then": "February"},
                                {"case": {"$eq": ["$month", 3]}, "then": "March"},
                                {"case": {"$eq": ["$month", 4]}, "then": "April"},
                                {"case": {"$eq": ["$month", 5]}, "then": "May"},
                                {"case": {"$eq": ["$month", 6]}, "then": "June"},
                                {"case": {"$eq": ["$month", 7]}, "then": "July"},
                                {"case": {"$eq": ["$month", 8]}, "then": "August"},
                                {"case": {"$eq": ["$month", 9]}, "then": "September"},
                                {"case": {"$eq": ["$month", 10]}, "then": "October"},
                                {"case": {"$eq": ["$month", 11]}, "then": "November"},
                                {"case": {"$eq": ["$month", 12]}, "then": "December"},
                            ],
                            "default": "Unknown",
                        },
                    },
                    "positive": "$positive",
                    "negative": "$negative",
                    "total": "$total"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "year": "$_id",
            "data": {
                "$slice": ["$data", 3]
            }
        }
    }
]
    result = client['hoteldb']['reviews '].aggregate(your_aggregation_pipeline)

    # Create a Tkinter window
    window = Tk()
    window.title("Sentiment Analysis Results")

    # Create labels to display the results
    label_info = Label(window, text="Sentiment Analysis Results:")

    # Create a text widget to display the results
    text_info = Text(window, height=50, wrap="word")

    # Create a scrollbar for the text widget
    scrollbar_info = Scrollbar(window)

    # Configure the scrollbar with the text widget
    text_info.config(yscrollcommand=scrollbar_info.set)

    # Pack the widgets to the window
    label_info.grid(row=0, column=0, sticky=W)
    text_info.grid(row=1, column=0, rowspan=5, sticky=N + S + E + W)
    scrollbar_info.grid(row=1, column=1, rowspan=5, sticky=N + S)

    # Insert data into the text widget
    for entry in result:
        #text_info.insert(END, f"• {entry['year']}:\n")
        if entry['year'] == int(xyear):
            for month_data in entry['data']:
                text_info.insert(END, f"  • {month_data['monthName']}:\n")
                text_info.insert(END, f"    • Positive: {month_data['positive']} reviews\n")
                text_info.insert(END, f"    • Negative: {month_data['negative']} reviews\n")
                text_info.insert(END, f"    • Total: {month_data['total']} reviews\n")

    # Run the Tkinter event loop
    window.mainloop()

def graph1():
    client = MongoClient('mongodb://localhost:27017/')
    result = client['hoteldb']['reviews '].aggregate([
    {
        '$project': {
            '_id': 0, 
            'reviews': 1
        }
    }, {
        '$unwind': '$reviews'
    }, {
        '$project': {
            'sentiment': {
                '$switch': {
                    'branches': [
                        {
                            'case': {
                                '$regexMatch': {
                                    'input': {
                                        '$concat': [
                                            '$reviews.text', ' ', '$reviews.title'
                                        ]
                                    }, 
                                    'regex': '(excellent|awesome|fantastic|amazing|outstanding|superb|terrific|pleasing|positive|perfect|great|wonderful|impressive|superior|exceptional|satisfying|delightful|splendid|stellar|commendable|first-rate|pleasurable|exquisite|admirable|noteworthy|brilliant|charming|enjoyable|marvelous|positive|pleasant|immaculate|gratifying|uplifting|heartwarming|affirmative|captivating|favorable|constructive|exuberant|good service|excellent service|attentive service|friendly staff|helpful staff|courteous staff|prompt service|efficient service|professional service|polite staff|fast service|positive experience|positive stay|positive impression|positive feedback|positive vibes|excellent room|awesome amenities|fantastic service|amazing location|outstanding staff|superb facilities|terrific experience|pleasing ambiance|positive atmosphere|perfect stay|great hospitality|wonderful view|impressive decor|superior cleanliness|exceptional quality|satisfying comfort|delightful surroundings|splendid decor|stellar service|commendable staff|first-rate amenities|pleasurable stay|exquisite design|admirable features|noteworthy comfort|brilliant arrangement|charming atmosphere|enjoyable environment|marvelous setting)', 
                                    'options': 'i'
                                }
                            }, 
                            'then': 'positive'
                        }, {
                            'case': {
                                '$regexMatch': {
                                    'input': {
                                        '$concat': [
                                            '$reviews.text', ' ', '$reviews.title'
                                        ]
                                    }, 
                                    'regex': '(poor|terrible|awful|horrible|disappointing|unpleasant|dreadful|inferior|negative|displeasing|unsatisfactory|disastrous|atrocious|appalling|lousy|mediocre|subpar|pitiful|regrettable|unfavorable|unpleasant|dismal|dreadful|discouraging|lamentable|gloomy|unfortunate|repugnant|offensive|disgusting|vile|abysmal|dreary|deplorable|disheartening|oppressive|woeful|unpleasant|objectionable|inferior|repulsive|poor service|bad service|inattentive service|unfriendly staff|unhelpful staff|rude staff|slow service|inefficient service|unprofessional service|discourteous staff|negative experience|negative stay|negative impression|negative feedback|negative vibes|poor room|terrible amenities|awful service|horrible location|disappointing staff|unpleasant facilities|dreadful experience|inferior ambiance|negative atmosphere|displeasing stay|unsatisfactory decor|disastrous cleanliness|atrocious surroundings|appalling decor|lousy service|mediocre amenities|subpar view|pitiful hospitality|regrettable features|unfavorable comfort|unpleasant surroundings|dismal arrangement|dreadful environment|discouraging setting|lamentable design|gloomy atmosphere|unfortunate features|repugnant hospitality|offensive staff|disgusting service|vile ambiance|abysmal environment|dreary setting|deplorable cleanliness|disheartening decor|oppressive surroundings|woeful facilities|unpleasant room|objectionable amenities|inferior features|repulsive comfort|poor service|bad service|inattentive service|unfriendly staff|unhelpful staff|rude staff|slow service|inefficient service|unprofessional service|discourteous staff|negative experience|negative stay|negative impression|negative feedback|negative vibes|poor room|terrible amenities|awful service|horrible location|disappointing staff|unpleasant facilities|dreadful experience|inferior ambiance|negative atmosphere|displeasing stay|unsatisfactory decor|disastrous cleanliness|atrocious surroundings|appalling decor|lousy service|mediocre amenities|subpar view|pitiful hospitality|regrettable features|unfavorable comfort|unpleasant surroundings|dismal arrangement|dreadful environment|discouraging setting|lamentable design|gloomy atmosphere|unfortunate features|repugnant hospitality|offensive staff|disgusting service|vile ambiance|abysmal environment|dreary setting|deplorable cleanliness|disheartening decor|oppressive surroundings|woeful facilities|unpleasant room|objectionable amenities|inferior features|repulsive comfort)', 
                                    'options': 'i'
                                }
                            }, 
                            'then': 'negative'
                        }, {
                            'case': {
                                '$regexMatch': {
                                    'input': {
                                        '$concat': [
                                            '$reviews.text', ' ', '$reviews.title'
                                        ]
                                    }, 
                                    'regex': '(average|mediocre|ordinary|standard|typical|neutral|middling|so-so|common|routine|regular|adequate|fair|tolerable|passable|acceptable|moderate)', 
                                    'options': 'i'
                                }
                            }, 
                            'then': 'average'
                        }
                    ], 
                    'default': 'unknown'
                }
            }, 
            'content': {
                '$concat': [
                    '$reviews.text', ' ', '$reviews.title'
                ]
            }, 
            'rating': '$reviews.rating'
        }
    }, {
        '$match': {
            'sentiment': {
                '$ne': 'unknown'
            }, 
            'rating': {
                '$in': [
                    1, 2, 3, 4, 5
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$sentiment', 
            'count': {
                '$sum': 1
            }
        }
    }
])

    result_list = list(result)
    _id_values = []  # List to store '_id' values
    count_values = []  # List to store 'count' values

    # Extracting '_id' and 'count' values
    for item in result_list:
        _id_values.append(item['_id'])
        count_values.append(item['count'])

    # Printing the extracted values
    print("_id:", _id_values)
    print("count:", count_values)

    positions=range(len(count_values))
    plt.bar(positions,count_values)
    plt.xticks(positions,_id_values)
    plt.title("REVIWED HOTELS BY REVIWERS")
    plt.xlabel("reviews")
    plt.ylabel("review count")
    plt.show()


    #xxx=np.random.normal(20000,25000,5000)
    #plt.bar(xxx,50)
    #plt.title("DATA")
    #plt.show()

my_button=tk.Button(root,text="hit me!",command=graph1)
my_button.pack()

label = tk.Label(root, text="Query2: in which year you want to present reviews")
label.pack()
options = ["2011", "2012", "2013", "2014","2015","2016","2017","2018","2019"]

dropdown = StringVar(root)
dropdown.set(options[0])  # Set the default value
def on_select(event):
    selected_value = dropdown.get()
    graph2(selected_value)

def on_province_selected(*args):
    selected_province = province_var.get()
    fetch_and_display_data(selected_province)

dropdown_menu = OptionMenu(root, dropdown, *options, command=on_select)
dropdown_menu.pack()
province_var = StringVar(root)

mongo_uri = 'mongodb://localhost:27017/'
database_name = 'hoteldb'
collection_name = 'reviews'
client = MongoClient(mongo_uri)
distinct_provinces = client[database_name][collection_name].distinct("province")
# province_var.set(distinct_provinces[0])  # Set the default province
try:
    province_var.set(distinct_provinces[0])
except IndexError:
    print("Index is out of range")
# Create an OptionMenu for province selection
province_label = Label(root, text="Query3: Select Province for all hotel reviews:")
province_label.pack()
province_menu = OptionMenu(root, province_var, *distinct_provinces)
province_menu.pack()

# Bind the event handler to the province variable
province_var.trace("w", on_province_selected)


label = tk.Label(root, text="Query4: For which month and province good hotel should be suggested")
label.pack()
# Province dropdown
province_label2 = tk.Label(root, text="Select Province:")
province_label2.pack(pady=5)
province_var2 = tk.StringVar()
province_dropdown2 = ttk.Combobox(root, textvariable=province_var2, values=get_unique_provinces())
province_dropdown2.pack(pady=5)

# Month dropdown
month_label = tk.Label(root, text="Select Month:")
month_label.pack(pady=5)
month_var = tk.StringVar()
month_dropdown = ttk.Combobox(root, textvariable=month_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
month_dropdown.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)



#my_button1=tk.Button(root,text="hit me!",command=graph2)
#my_button1.pack()


# Start the main event loop
root.mainloop()
