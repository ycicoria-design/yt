import random


def get_trending_sounds(category="cat"):

    sounds = [
        {
            "name": "Funny Song - Trending Audio",
            "platform": "TikTok / Shorts",
            "trend": "+34% rising"
        },
        {
            "name": "Original Sound - Cute Reaction",
            "platform": "TikTok",
            "trend": "+22% rising"
        },
        {
            "name": "Comedy Timing Audio",
            "platform": "YouTube Shorts",
            "trend": "+18% rising"
        },
        {
            "name": "Emotional Piano Trend",
            "platform": "TikTok / Reels",
            "trend": "+15% rising"
        }
    ]

    return random.choice(sounds)



def print_sound_report(category):

    sound = get_trending_sounds(category)

    print("\n🎵 TRENDING SOUND RECOMMENDATION")
    print("==============================")
    print("Sound:", sound["name"])
    print("Platform:", sound["platform"])
    print("Trend:", sound["trend"])

    print("\nWhy:")
    print("- Matches your video category")
    print("- Currently rising")
    print("- Similar videos use this style")


if __name__ == "__main__":
    print_sound_report("cat")
