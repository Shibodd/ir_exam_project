def parse_post_title(title: str):
    anime_title,episode_part=title.split(" - Episode ")
    anime_episode=episode_part.removesuffix(" discussion")
    anime_episode=int(anime_episode)
    return (anime_title,anime_episode)