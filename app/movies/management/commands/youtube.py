import youtube_dl

URLS = [
    ('20193069', 'https://youtu.be/ifyPEnKreJI'),
    ('20183813', 'https://youtu.be/5QWeKTO9NpY'),
    ('20196201', 'https://youtu.be/86RYz4Qb8VQ'),
    ('20081056', 'https://youtu.be/ty1XzpkAAQA'),
    ('20191048', 'https://youtu.be/7CyeDl6wNok'),
    ('20208617', 'https://youtu.be/9LXmYtZEnUQ'),
    ('20200361', 'https://youtu.be/2DPU-KJqviY'),
    ('20179462', 'https://youtu.be/cnIOq6P8PUU'),
    ('20196702', 'https://youtu.be/tHgzM5RM-JY'),
    ('20201841', 'https://youtu.be/qXwMWUCwvXM'),
]

for URL in URLS:
    ydl_opts = {
        'outtmpl': f'~/Downloads/{URL[0]}.mp4'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL[1]])
