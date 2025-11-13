# SoundCloud Scraper
A fast and dependable SoundCloud scraper that retrieves detailed information about tracks, playlists, albums, users, and comments. It helps you extract structured metadata, discover downloadable media, and access deep-level insights that aren’t available through typical interfaces. This solution is ideal for researchers, analysts, and developers who need scalable SoundCloud data collection.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>SoundCloud Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
This project collects comprehensive data from SoundCloud pages and returns it in a clean, structured format.
It solves the challenge of gathering music metadata, user insights, and comment threads without limitations.
It is designed for analysts, data engineers, digital marketers, and anyone seeking high-volume SoundCloud data with ease.

### How It Works
- Accepts multiple SoundCloud URLs such as track, playlist, album, user, or search endpoints.
- Extracts track metadata, user information, media URLs, and comment threads.
- Supports filtering by page count and maximum items to control scraping depth.
- Handles public SoundCloud content efficiently with minimal overhead.

## Features
| Feature | Description |
|---------|-------------|
| Multi-type URL Support | Works with track, user, playlist, album, and search URLs. |
| Track Metadata Extraction | Retrieves duration, title, genre, playback count, likes, reposts, license, and more. |
| Comment Collection | Retrieves comments with timestamps, user info, and message details. |
| User Information Extraction | Captures avatar, follower count, username, badges, and verification status. |
| Download URL Discovery | Extracts available download URLs for tracks. |
| Pagination Control | Supports `endPage` to limit scraping depth and page intervals. |
| Output Dataset Mode | Stores each scraped item as a structured dataset entry. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|------------|------------------|
| artwork_url | URL to the track’s artwork image. |
| caption | Caption added by the uploader. |
| comment_count | Total number of comments. |
| created_at | Timestamp of track creation. |
| description | Full track description text. |
| duration | Length of the track in milliseconds. |
| genre | Genre category of the track. |
| id | Unique SoundCloud track ID. |
| likes_count | Number of likes. |
| permalink_url | Public URL to the track. |
| playback_count | Number of plays. |
| purchase_url | External purchase or sign-up link. |
| reposts_count | Total reposts. |
| title | Track title. |
| uri | API resource URI for the track. |
| user | Embedded object with user details. |
| comments | Array of comment objects including user details and timestamps. |
| media | Streaming and download transcoding metadata. |

---

## Example Output


    [
      {
        "artwork_url": "https://i1.sndcdn.com/artworks-KUd5CFXdByl4gCVn-qYc5Ug-large.jpg",
        "comment_count": 754,
        "created_at": "2023-01-24T13:15:38Z",
        "description": "🚨SUBSCRIBE: bit.ly/DnbaSubscribe",
        "duration": 3558922,
        "genre": "Drum & Bass",
        "id": 1431326908,
        "likes_count": 13904,
        "permalink_url": "https://soundcloud.com/dnballstars/hedex-dnb-allstars-360",
        "playback_count": 307681,
        "title": "Hedex - DnB Allstars 360°",
        "user": {
          "username": "DnB Allstars",
          "followers_count": 84897,
          "verified": true
        },
        "comments": [
          {
            "body": "Oh my days 😳😳😳",
            "timestamp": 326931,
            "user": { "username": "User 655659681" }
          }
        ]
      }
    ]

---

## Directory Structure Tree


    SoundCloud Scraper/
    ├── src/
    │   ├── main.py
    │   ├── core/
    │   │   ├── soundcloud_client.py
    │   │   ├── parser_tracks.py
    │   │   ├── parser_users.py
    │   │   ├── parser_playlists.py
    │   │   └── parser_comments.py
    │   ├── utils/
    │   │   ├── url_validator.py
    │   │   └── pagination.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── sample_output.json
    │   └── inputs.sample.json
    ├── requirements.txt
    └── README.md

---

## Use Cases
- **Music analysts** use it to monitor artists and track performance trends, enabling smarter insights.
- **Digital marketers** use it to research audience engagement, helping them optimize campaigns and content.
- **Developers** integrate it into data pipelines to automate music metadata indexing.
- **Researchers** use it to study genre trends, comment behavior, or cultural signals within music communities.
- **Media companies** use it to gather structured metadata for recommendation engines or editorial curation.

---

## FAQs

**Q: What SoundCloud links can I use?**
A: You can provide track links, playlists, user pages, album pages, or search queries. The scraper will interpret and extract valid data accordingly.

**Q: Can it collect comments?**
A: Yes. If enabled, it retrieves all available comments along with timestamps, user info, and engagement metadata.

**Q: How do I limit how much data is scraped?**
A: Use `endPage` to stop scraping after a certain number of pages and `maxItems` to cap total extracted items.

**Q: Does it work with large lists or search pages?**
A: Yes, it efficiently handles multi-page results and large datasets by streaming data in a stable and optimized manner.

---

## Performance Benchmarks and Results
- **Primary Metric:** Scrapes up to 100 tracks in roughly 2 minutes under typical conditions.
- **Reliability Metric:** Maintains a high success rate across mixed URL types with stable request handling.
- **Efficiency Metric:** Consistent low resource consumption even when collecting comments or processing long playlists.
- **Quality Metric:** Produces complete, deeply structured metadata including media, user, and comment details for high-precision analysis.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
