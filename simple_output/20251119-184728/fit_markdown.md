[Skip to content](https://github.com/unclecode/crawl4ai#start-of-content)
You signed in with another tab or window. to refresh your session. You signed out in another tab or window. to refresh your session. You switched accounts on another tab or window. to refresh your session.
  * You must be signed in to change notification settings


🚀🤖 Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper. Don't be shy, join here: 
You must be signed in to change notification settings
Go to file
Open more actions menu
## Folders and files
Last commit message | Last commit date  
---|---  
View all files  
## Repository files navigation
# 🚀🤖 Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper.
Crawl4AI turns the web into clean, LLM ready Markdown for RAG, agents, and data pipelines. Fast, controllable, battle tested by a 50k+ star community.
[✨ Check out latest update v0.7.7](https://github.com/unclecode/crawl4ai#-recent-updates)
✨ **New in v0.7.7** : Complete Self-Hosting Platform with Real-time Monitoring! Enterprise-grade monitoring dashboard, comprehensive REST API, WebSocket streaming, smart browser pool management, and production-ready observability. Full visibility and control over your crawling infrastructure. [Release notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.7.md)
✨ Recent v0.7.6: Complete Webhook Infrastructure for Docker Job Queue API! Real-time notifications for both and endpoints with exponential backoff retry, custom headers, and flexible delivery modes. No more polling! [Release notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.6.md)
✨ Previous v0.7.5: Docker Hooks System with function-based API for pipeline customization, Enhanced LLM Integration with custom providers, HTTPS Preservation, and multiple community-reported bug fixes. [Release notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.5.md)
🤓 **My Personal Story**
I grew up on an Amstrad, thanks to my dad, and never stopped building. In grad school I specialized in NLP and built crawlers for research. That’s where I learned how much extraction matters.
In 2023, I needed web-to-Markdown. The “open source” option wanted an account, API token, and $16, and still under-delivered. I went turbo anger mode, built Crawl4AI in days, and it went viral. Now it’s the most-starred crawler on GitHub.
I made it open source for , anyone can use it without a gate. Now I’m building the platform for , anyone can run serious crawls without breaking the bank. If that resonates, join in, send feedback, or just crawl something amazing.
Why developers pick Crawl4AI
  * **LLM ready output** , smart Markdown with headings, tables, code, citation hints
  * **Fast in practice** , async browser pool, caching, minimal hops
  * , sessions, proxies, cookies, user scripts, hooks
  * , learns site patterns, explores only what matters
  * , zero keys, CLI and Docker, cloud friendly


## 🚀 Quick Start
```
 Install the package
pip install -U crawl4ai

 For pre release versions
pip install crawl4ai --pre

 Run post-installation setup
crawl4ai-setup

 Verify your installation
crawl4ai-doctor
```

If you encounter any browser-related issues, you can install them manually:
```
python -m playwright install --with-deps chromium
```

  1. Run a simple web crawl with Python:


```
 
   

  ():
      ()  :
           .(
            ,
        )
        (.)

   :
    .(())
```

  1. Or use the new command-line interface:


```
 Basic crawl with markdown output
crwl https://www.nbcnews.com/business -o markdown

 Deep crawl with BFS strategy, max 10 pages
crwl https://docs.crawl4ai.com --deep-crawl bfs --max-pages 10

 Use LLM extraction with a specific question
crwl https://www.example.com/products -q Extract all product prices
```

## 💖 Support Crawl4AI
> 🎉 **Sponsorship Program Now Open!** After powering 51K+ developers and 1 year of growth, Crawl4AI is launching dedicated support for and . Be among the first 50 for permanent recognition in our Hall of Fame.
Crawl4AI is the #1 trending open-source web crawler on GitHub. Your support keeps it independent, innovative, and free for the community — while giving you direct access to premium benefits.
### 🤝 Sponsorship Tiers
  * **🌱 Believer ($5/mo)** — Join the movement for data democratization
  * **🚀 Builder ($50/mo)** — Priority support & early access to features
  * **💼 Growing Team ($500/mo)** — Bi-weekly syncs & optimization help
  * **🏢 Data Infrastructure Partner ($2000/mo)** — Full partnership with dedicated support _Custom arrangements available - see for details & contact_


No rate-limited APIs. No lock-in. Build and own your data pipeline with direct guidance from the creator of Crawl4AI.
[See All Tiers & Benefits →](https://github.com/sponsors/unclecode)
  * 🧹 : Generates clean, structured Markdown with accurate formatting.
  * 🎯 : Heuristic-based filtering to remove noise and irrelevant parts for AI-friendly processing.
  * 🔗 **Citations and References** : Converts page links into a numbered reference list with clean citations.
  * 🛠️ : Users can create their own Markdown generation strategies tailored to specific needs.
  * 📚 : Employs BM25-based filtering for extracting core information and removing irrelevant content.

📊 **Structured Data Extraction**
  * 🤖 : Supports all LLMs (open-source and proprietary) for structured data extraction.
  * 🧱 : Implements chunking (topic-based, regex, sentence-level) for targeted content processing.
  * 🌌 : Find relevant content chunks based on user queries for semantic extraction.
  * 🔎 : Fast schema-based data extraction using XPath and CSS selectors.
  * 🔧 : Define custom schemas for extracting structured JSON from repetitive patterns.


  * 🖥️ : Use user-owned browsers with full control, avoiding bot detection.
  * 🔄 **Remote Browser Control** : Connect to Chrome Developer Tools Protocol for remote, large-scale data extraction.
  * 👤 : Create and manage persistent profiles with saved authentication states, cookies, and settings.
  * 🔒 : Preserve browser states and reuse them for multi-step crawling.
  * 🧩 : Seamlessly connect to proxies with authentication for secure access.
  * ⚙️ **Full Browser Control** : Modify headers, cookies, user agents, and more for tailored crawling setups.
  * 🌍 : Compatible with Chromium, Firefox, and WebKit.
  * 📐 **Dynamic Viewport Adjustment** : Automatically adjusts the browser viewport to match page content, ensuring complete rendering and capturing of all elements.

🔎 **Crawling & Scraping**
  * 🖼️ : Extract images, audio, videos, and responsive image formats like and .
  * 🚀 : Execute JS and wait for async or sync for dynamic content extraction.
  * 📸 : Capture page screenshots during crawling for debugging or analysis.
  * 📂 **Raw Data Crawling** : Directly process raw HTML () or local files ().
  * 🔗 **Comprehensive Link Extraction** : Extracts internal, external links, and embedded iframe content.
  * 🛠️ : Define hooks at every step to customize crawling behavior (supports both string and function-based APIs).
  * 💾 : Cache data for improved speed and to avoid redundant fetches.
  * 📄 : Retrieve structured metadata from web pages.
  * 📡 **IFrame Content Extraction** : Seamless extraction from embedded iframe content.
  * 🕵️ **Lazy Load Handling** : Waits for images to fully load, ensuring no content is missed due to lazy loading.
  * 🔄 : Simulates scrolling to load and capture all dynamic content, perfect for infinite scroll pages.


  * 🐳 : Optimized Docker image with FastAPI server for easy deployment.
  * 🔑 : Built-in JWT token authentication for API security.
  * 🔄 : One-click deployment with secure token authentication for API-based workflows.
  * 🌐 : Designed for mass-scale production and optimized server performance.
  * ☁️ : Ready-to-deploy configurations for major cloud platforms.


  * 🕶️ : Avoid bot detection by mimicking real users.
  * 🏷️ **Tag-Based Content Extraction** : Refine crawling based on custom tags, headers, or metadata.
  * 🔗 : Extract and analyze all links for detailed data exploration.
  * 🛡️ : Robust error management for seamless execution.
  * 🔐 **CORS & Static Serving**: Supports filesystem-based caching and cross-origin requests.
  * 📖 : Simplified and updated guides for onboarding and advanced usage.
  * 🙌 : Acknowledges contributors and pull requests for transparency.


## Try it Now!
✨ Play around with this 
✨ Visit our 
Crawl4AI offers flexible installation options to suit various use cases. You can install it as a Python package or use Docker.
Choose the installation option that best fits your needs:
For basic web crawling and scraping tasks:
```
pip install crawl4ai
crawl4ai-setup  Setup the browser
```

By default, this will install the asynchronous version of Crawl4AI, using Playwright for web crawling.
👉 : When you install Crawl4AI, the should automatically install and set up Playwright. However, if you encounter any Playwright-related errors, you can manually install it using one of these methods:
  1. Through the command line:
  2. If the above doesn't work, try this more specific command:
```
python -m playwright install chromium
```



This second method has proven to be more reliable in some cases.
### Installation with Synchronous Version
The sync version is deprecated and will be removed in future versions. If you need the synchronous version using Selenium:
```
pip install crawl4ai[sync]
```

For contributors who plan to modify the source code:
```
git clone https://github.com/unclecode/crawl4ai.git
 crawl4ai
pip install -e                      Basic installation in editable mode
```

Install optional features:
```
pip install -e             With PyTorch features
pip install -e       With Transformer features
pip install -e            With cosine similarity features
pip install -e              With synchronous crawling (Selenium)
pip install -e               Install all optional features
```

> 🚀 Our completely redesigned Docker implementation is here! This new solution makes deployment more efficient and seamless than ever.
### New Docker Features
The new Docker implementation includes:
  * **Real-time Monitoring Dashboard** with live system metrics and browser pool visibility
  * with page pre-warming for faster response times
  * to test and generate request code
  * for direct connection to AI tools like Claude Code
  * **Comprehensive API endpoints** including HTML extraction, screenshots, PDF generation, and JavaScript execution
  * with automatic detection (AMD64/ARM64)
  * with improved memory management


```
 Pull and run the latest release
docker pull unclecode/crawl4ai:latest
docker run -d -p 11235:11235 --name crawl4ai --shm-size=1g unclecode/crawl4ai:latest

 Visit the monitoring dashboard at http://localhost:11235/dashboard
 Or the playground at http://localhost:11235/playground
```

Run a quick test (works for both Docker options):
```
 

# Submit a crawl job
  .(
    ,
    {: [], : }
)
 .  :
    ("Crawl job submitted successfully.")
    
   .():
      .()[]
    ("Crawl job completed. Results:")
       :
        ()
:
      .()[]
    (f"Crawl job submitted. Task ID:: ")
      .()
```

For more examples, see our . For advanced configuration, monitoring features, and production deployment, see our .
## 🔬 Advanced Usage Examples 🔬
You can check the project structure in the directory . Over there, you can find a variety of examples; here, some popular examples are shared.
📝 **Heuristic Markdown Generation with Clean and Fit Markdown**
```
 
   , , , 
 .  , 
 .  

  ():
      (
        ,  
        ,
    )
      (
        .,
        (
            (, , )
        ),
        
        #     content_filter=BM25ContentFilter(user_query="WHEN_WE_FOCUS_BASED_ON_A_USER_QUERY", bm25_threshold=1.0)
        
    )
    
      ()  :
           .(
            ,
            
        )
        ((..))
        ((..))

   :
    .(())
```

🖥️ **Executing JavaScript & Extract Structured Data without LLMs**
```
 
   , , , 
   
 

  ():
      {
    : ,
    : "section.charge-methodology .w-tab-content > div",
    : [
        {
            : ,
            : ,
            : ,
        },
        {
            : ,
            : ,
            : ,
        },
        {
            : ,
            : ,
            : ,
        },
        {
            : ,
            : ,
            : ,
        },
        {
            : ,
            : ,
            : ,
            : 
        }
    ]
}

      (, )

      (
        ,
        
    )
      (
        ,
        ["""(async () => {const tabs = document.querySelectorAll("section.charge-methodology .tabs-menu-3 > div");for(let tab of tabs) {tab.scrollIntoView();tab.click();await new Promise(r => setTimeout(r, 500));}})();"""],
        .
    )
        
      ()  :
        
           .(
            ,
            
        )

          .(.)
        ()
        (.([], ))


   :
    .(())
```

📚 **Extracting Structured Data with LLMs**
```
 
 
   , , , , 
   
   , 

 ():
    :   (..., "Name of the OpenAI model.")
    :   (..., "Fee for input token for the OpenAI model.")
    :   (..., "Fee for output token for the OpenAI model.")

  ():
      ()
      (
        ,
        (
            # Here you can use any provider that Litellm library supports, for instance: ollama/qwen2
            # provider="ollama/qwen2", api_token="no-token", 
              (, .()), 
            .(),
            ,
            """From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content. One extracted model JSON format should look like this: 
            {"model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens"}."""
        ),            
        .,
    )
    
      ()  :
           .(
            ,
            
        )
        (.)

   :
    .(())
```

🤖 **Using Your own Browser with Custom User Profile**
```
 , 
   
 , 
   , , , 

  ():
    # Create a persistent user data directory
      ..(.(), , )
    .(, )

      (
        ,
        ,
        ,
        ,
    )
      (
        .
    )
    
      ()  :
          
        
           .(
            ,
            ,
            ,
        )
        
        ()
        ()
```

> Some websites may use based verification mechanisms to prevent automated access. If your workflow encounters such challenges, you may optionally integrate a third-party CAPTCHA-handling service such as . They support reCAPTCHA v2/v3, Cloudflare Turnstile, Challenge, AWS WAF, and more. Please ensure that your usage complies with the target website’s terms of service and applicable laws.
## ✨ Recent Updates
**Version 0.7.7 Release Highlights - The Self-Hosting & Monitoring Update**
  * **📊 Real-time Monitoring Dashboard** : Interactive web UI with live system metrics and browser pool visibility
```
# Access the monitoring dashboard
# Visit: http://localhost:11235/dashboard

# Real-time metrics include:
# - System health (CPU, memory, network, uptime)
# - Active and completed request tracking
# - Browser pool management (permanent/hot/cold)
# - Janitor cleanup events
# - Error monitoring with full context
```

  * **🔌 Comprehensive Monitor API** : Complete REST API for programmatic access to all monitoring data
```
 

  .()  :
    # System health
       .()

    # Request tracking
       .()

    # Browser pool status
       .()

    # Endpoint statistics
       .()
```

  * **⚡ WebSocket Streaming** : Real-time updates every 2 seconds for custom dashboards
  * **🔥 Smart Browser Pool** : 3-tier architecture (permanent/hot/cold) with automatic promotion and cleanup
  * **🧹 Janitor System** : Automatic resource management with event logging
  * **🎮 Control Actions** : Manual browser management (kill, restart, cleanup) via API
  * **📈 Production Metrics** : 6 critical metrics for operational excellence with Prometheus integration
  * **🐛 Critical Bug Fixes** :
    * Fixed async LLM extraction blocking issue (#1055)
    * Enhanced DFS deep crawl strategy (#1607)
    * Fixed sitemap parsing in AsyncUrlSeeder (#1598)
    * Resolved browser viewport configuration (#1495)
    * Fixed CDP timing with exponential backoff (#1528)
    * Security update for pyOpenSSL (>=25.3.0)


[Full v0.7.7 Release Notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.7.md)
**Version 0.7.5 Release Highlights - The Docker Hooks & Security Update**
  * **🔧 Docker Hooks System** : Complete pipeline customization with user-provided Python functions at 8 key points
  * **✨ Function-Based Hooks API (NEW)** : Write hooks as regular Python functions with full IDE support:
```
   
 .  

# Define hooks as regular Python functions
  (, , ):
    """Block images to speed up crawling"""
     .(,  : .())
     .({: , : })
     

  (, , , ):
    """Add custom headers"""
     .({: })
     

# Option 1: Use hooks_to_string() utility for REST API
  ({
    : ,
    : 
})

# Option 2: Docker client with automatic conversion (Recommended)
  ()
   .(
    [],
    {
        : ,
        : 
    }
)
# ✓ Full IDE support, type checking, and reusability!
```

  * **🤖 Enhanced LLM Integration** : Custom providers with temperature control and base_url configuration
  * **🔒 HTTPS Preservation** : Secure internal link handling with 
  * **🐍 Python 3.10+ Support** : Modern language features and enhanced performance
  * **🛠️ Bug Fixes** : Resolved multiple community-reported issues including URL processing, JWT authentication, and proxy configuration


[Full v0.7.5 Release Notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.5.md)
**Version 0.7.4 Release Highlights - The Intelligent Table Extraction & Performance Update**
  * : Revolutionary table extraction with intelligent chunking for massive tables:
```
   , 

# Configure intelligent table extraction
  (
    (),
    ,           # Handle massive tables
    ,     # Smart chunking threshold
    ,          # Maintain context between chunks
        # Get structured data output
)

  ()
   .(, )

# Tables are automatically chunked, processed, and merged
   .:
    ()
```

  * **⚡ Dispatcher Bug Fix** : Fixed sequential processing bottleneck in arun_many for fast-completing tasks
  * **🧹 Memory Management Refactor** : Consolidated memory utilities into main utils module for cleaner architecture
  * **🔧 Browser Manager Fixes** : Resolved race conditions in concurrent page creation with thread-safe locking
  * **🔗 Advanced URL Processing** : Better handling of raw:// URLs and base tag link resolution
  * **🛡️ Enhanced Proxy Support** : Flexible proxy configuration supporting both dict and string formats


[Full v0.7.4 Release Notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.4.md)
**Version 0.7.3 Release Highlights - The Multi-Config Intelligence Update**
  * **🕵️ Undetected Browser Support** : Bypass sophisticated bot detection systems:
```
   , 

  (
    ,  # Use undetected Chrome
    ,              # Can run headless with stealth
    [
        ,
        
    ]
)

  ()  :
       .()
# Successfully bypass Cloudflare, Akamai, and custom bot detection
```

  * **🎨 Multi-URL Configuration** : Different strategies for different URL patterns in one batch:
```
   , 

  [
    # Documentation sites - aggressive caching
    (
        [, ],
        ,
        {: }
    ),
    
    # News/blog sites - fresh content
    (
         :       ,
        
    ),
    
    # Fallback for everything else
    ()
]

   .(, )
# Each URL gets the perfect configuration automatically
```

  * **🧠 Memory Monitoring** : Track and optimize memory usage during crawling:
```
 .  

  ()
.()

   .()

  .()
()
()
# Get optimization recommendations
```

  * **📊 Enhanced Table Extraction** : Direct DataFrame conversion from web tables:
```
   .()

# New way - direct table access
 .:
       
       .:
          .([])
        ()
```

  * **💰 GitHub Sponsors** : 4-tier sponsorship system for project sustainability
  * **🐳 Docker LLM Flexibility** : Configure providers via environment variables


[Full v0.7.3 Release Notes →](https://github.com/unclecode/crawl4ai/blob/main/docs/blog/release-v0.7.3.md)
**Version 0.7.0 Release Highlights - The Adaptive Intelligence Update**
  * **🧠 Adaptive Crawling** : Your crawler now learns and adapts to website patterns automatically:
```
  (
    , # Min confidence to stop crawling
    , # Maximum crawl depth
    , # Maximum number of pages to crawl
    
)

  ()  :
      (, )
       .(
        ,
        "latest news content"
    )
# Crawler learns patterns and improves extraction over time
```

  * **🌊 Virtual Scroll Support** : Complete content extraction from infinite scroll pages:
  * **🔗 Intelligent Link Analysis** : 3-layer scoring system for smart link prioritization:
```
  (
    "machine learning tutorials",
    ,
    
)

   .(, (
    ,
    
))
# Links ranked by relevance and quality
```

  * **🎣 Async URL Seeder** : Discover thousands of URLs in seconds:
  * **⚡ Performance Boost** : Up to 3x faster with optimized resource handling and memory efficiency


Read the full details in our [0.7.0 Release Notes](https://docs.crawl4ai.com/blog/release-v0.7.0) or check the .
## Version Numbering in Crawl4AI
Crawl4AI follows standard Python version numbering conventions (PEP 440) to help users understand the stability and features of each release.
📈 **Version Numbers Explained**
Our version numbers follow this pattern: (e.g., 0.4.3)
We use different suffixes to indicate development stages:
  * (0.4.3dev1): Development versions, unstable
  * (0.4.3a1): Alpha releases, experimental features
  * (0.4.3b1): Beta releases, feature complete but needs testing
  * (0.4.3): Release candidates, potential final version


  * Regular installation (stable version):
```
pip install -U crawl4ai
```

  * Install pre-release versions:
```
pip install crawl4ai --pre
```

  * Install specific version:
```
pip install crawl4ai==0.4.3b1
```



We use pre-releases to:
  * Test new features in real-world scenarios
  * Gather feedback before final releases
  * Ensure stability for production users
  * Allow early adopters to try new features


For production environments, we recommend using the stable version. For testing new features, you can opt-in to pre-releases using the flag.
## 📖 Documentation & Roadmap
> 🚨 **Documentation Update Alert** : We're undertaking a major documentation overhaul next week to reflect recent updates and improvements. Stay tuned for a more comprehensive and up-to-date guide!
For current documentation, including installation instructions, advanced features, and API reference, visit our .
To check our development plans and upcoming features, visit our .
  * 0. Graph Crawler: Smart website traversal using graph search algorithms for comprehensive nested page extraction
  * 1. Question-Based Crawler: Natural language driven web discovery and content extraction
  * 2. Knowledge-Optimal Crawler: Smart crawling that maximizes knowledge while minimizing data extraction
  * 3. Agentic Crawler: Autonomous system for complex multi-step crawling operations
  * 4. Automated Schema Generator: Convert natural language to extraction schemas
  * 5. Domain-Specific Scrapers: Pre-configured extractors for common platforms (academic, e-commerce)
  * 6. Web Embedding Index: Semantic search infrastructure for crawled content
  * 7. Interactive Playground: Web UI for testing, comparing strategies with AI assistance
  * 8. Performance Monitor: Real-time insights into crawler operations
  * 9. Cloud Integration: One-click deployment solutions across cloud providers
  * 10. Sponsorship Program: Structured support system with tiered benefits
  * 11. Educational Content: "How to Crawl" video series and interactive tutorials


We welcome contributions from the open-source community. Check out our for more information.
I'll help modify the license section with badges. For the halftone effect, here's a version with it:
Here's the updated license section:
## 📄 License & Attribution
This project is licensed under the Apache License 2.0, attribution is recommended via the badges below. See the [Apache 2.0 License](https://github.com/unclecode/crawl4ai/blob/main/LICENSE) file for details.
When using Crawl4AI, you must include one of the following attribution methods:
📈 **1. Badge Attribution (Recommended)** Add one of these badges to your README, documentation, or website:  **Disco Theme (Animated)**  
---  
**Night Theme (Dark with Neon)**  
**Dark Theme (Classic)**  
**Light Theme (Classic)**  
HTML code for adding the badges:
```
<!-- Disco Theme (Animated) -->
 =""
   ="" ="Powered by Crawl4AI" =""


<!-- Night Theme (Dark with Neon) -->
 =""
   ="" ="Powered by Crawl4AI" =""


<!-- Dark Theme (Classic) -->
 =""
   ="" ="Powered by Crawl4AI" =""


<!-- Light Theme (Classic) -->
 =""
   ="" ="Powered by Crawl4AI" =""


<!-- Simple Shield Badge -->
 =""
   ="" ="Powered by Crawl4AI"

```

📖 **2. Text Attribution** Add this line to your documentation: ``` This project uses Crawl4AI () for web data extraction. ``` 
If you use Crawl4AI in your research or project, please cite:
```
{,
   = ,
   = Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper,
   = ,
   = ,
   = ,
   = ,
   = Please use the commit hash you're working with
}
```

Text citation format:
```
UncleCode. (2024). Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper [Computer software]. 
GitHub. https://github.com/unclecode/crawl4ai

```

For questions, suggestions, or feedback, feel free to reach out:
Happy Crawling! 🕸️🚀
Our mission is to unlock the value of personal and enterprise data by transforming digital footprints into structured, tradeable assets. Crawl4AI empowers individuals and organizations with open-source tools to extract and structure data, fostering a shared data economy.
We envision a future where AI is powered by real human knowledge, ensuring data creators directly benefit from their contributions. By democratizing data and enabling ethical sharing, we are laying the foundation for authentic AI advancement.
  * : Transform digital footprints into measurable, valuable assets.
  * **Authentic AI Data** : Provide AI systems with real human insights.
  * : Create a fair data marketplace that benefits data creators.


  1. : Community-driven platforms for transparent data extraction.
  2. **Digital Asset Structuring** : Tools to organize and value digital knowledge.
  3. **Ethical Data Marketplace** : A secure, fair platform for exchanging structured data.


For more details, see our [full mission statement](https://github.com/unclecode/crawl4ai/blob/main/MISSION.md).
## 🌟 Current Sponsors
### 🏢 Enterprise Sponsors & Partners
Our enterprise sponsors and technology partners help scale Crawl4AI to power production-grade data pipelines.
Scrapeless is the best full-stack web scraping toolkit offering Scraping API, Scraping Browser, Web Unlocker, Captcha Solver, and Proxies, designed to handle all your data collection needs.  
---  
AI-powered Captcha solving service. Supports all major Captcha types, including reCAPTCHA, Cloudflare, and more  
Helps engineers and buyers find, compare, and source electronic & industrial parts in seconds, with specs, pricing, lead times & alternatives.  
Kidocode is a hybrid technology and entrepreneurship school for kids aged 5–18, offering both online and on-campus education.  
Singapore-based Aleph Null is Asia’s leading edtech hub, dedicated to student-centric, AI-driven education—empowering learners with the tools to thrive in a fast-changing world.  
### 🧑‍🤝 Individual Sponsors
A heartfelt thanks to our individual supporters! Every contribution helps us keep our opensource mission alive and thriving!
> Want to join them? [Sponsor Crawl4AI →](https://github.com/sponsors/unclecode)
🚀🤖 Crawl4AI: Open-source LLM Friendly Web Crawler & Scraper. Don't be shy, join here: 
### Code of conduct
There was an error while loading. [Please reload this page](https://github.com/unclecode/crawl4ai).
[ Nov 14, 2025 ](https://github.com/unclecode/crawl4ai/releases/tag/v0.7.7)
[+ 10 releases](https://github.com/unclecode/crawl4ai/releases)
## Sponsor this project
[Learn more about GitHub Sponsors](https://github.com/sponsors)
No packages published 
[+ 45 contributors](https://github.com/unclecode/crawl4ai/graphs/contributors)
