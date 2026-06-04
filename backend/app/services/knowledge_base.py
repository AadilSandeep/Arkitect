"""
Domain Knowledge Base — the deterministic intelligence engine for Arkitect.

This module contains curated lookup tables that map user goals to structured
outputs: domains, deliverables, tools, workflow templates, knowledge areas,
alternative strategies, and time estimates.

Coverage: Web Development, Mobile Development, Data Science, Content Creation,
Marketing, Game Development, E-Commerce, DevOps.

Design rationale:
- All data is static and deterministic — no AI calls required.
- Services query these tables via keyword matching.
- Easy to extend: add a new domain by adding entries to each dict.
- When Gemini integration lands, these tables serve as fallback/seed data.
"""

# ---------------------------------------------------------------------------
# DOMAIN KEYWORDS
# Maps lowercase keywords → domain name.
# The GoalAnalyzer tokenizes user input and counts keyword hits per domain.
# ---------------------------------------------------------------------------

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "Web Development": [
        "website", "web", "webapp", "web app", "frontend", "backend",
        "fullstack", "full-stack", "html", "css", "javascript", "react",
        "vue", "angular", "nextjs", "next.js", "node", "express",
        "portfolio", "landing page", "blog", "dashboard", "saas",
        "api", "rest", "graphql", "tailwind", "bootstrap",
    ],
    "Mobile Development": [
        "mobile", "android", "ios", "app", "flutter", "react native",
        "swift", "kotlin", "mobile app", "phone", "tablet",
        "cross-platform", "native app", "expo",
    ],
    "Data Science": [
        "data", "machine learning", "ml", "ai", "deep learning",
        "neural network", "model", "dataset", "analytics", "pandas",
        "numpy", "tensorflow", "pytorch", "scikit", "jupyter",
        "prediction", "classification", "regression", "nlp",
        "computer vision", "data science", "data analysis",
    ],
    "Content Creation": [
        "youtube", "video", "content", "podcast", "blog", "vlog",
        "streaming", "twitch", "tiktok", "instagram", "creator",
        "editing", "thumbnail", "channel", "subscriber",
        "content creation", "film", "animation", "shorts",
    ],
    "Marketing": [
        "marketing", "seo", "social media", "ads", "advertising",
        "campaign", "brand", "branding", "email marketing", "growth",
        "funnel", "conversion", "copywriting", "newsletter",
        "influencer", "audience", "engagement", "digital marketing",
    ],
    "Game Development": [
        "game", "gaming", "unity", "unreal", "godot", "2d", "3d",
        "game dev", "game development", "multiplayer", "fps", "rpg",
        "indie game", "game design", "pixel art", "sprite",
        "game engine", "level design",
    ],
    "E-Commerce": [
        "ecommerce", "e-commerce", "store", "shop", "shopify",
        "woocommerce", "product", "inventory", "payment", "cart",
        "checkout", "marketplace", "sell", "online store",
        "dropshipping", "subscription",
    ],
    "DevOps": [
        "devops", "deploy", "deployment", "ci/cd", "cicd", "docker",
        "kubernetes", "k8s", "aws", "cloud", "terraform", "ansible",
        "jenkins", "github actions", "monitoring", "infrastructure",
        "server", "linux", "nginx", "pipeline",
    ],
}


# ---------------------------------------------------------------------------
# GOAL TYPE PATTERNS
# Maps keyword patterns → goal type classification.
# Checked after domain detection to refine the goal_type field.
# ---------------------------------------------------------------------------

GOAL_TYPE_PATTERNS: dict[str, list[str]] = {
    "Portfolio Website": ["portfolio", "personal website", "personal site"],
    "Landing Page": ["landing page", "landing", "launch page"],
    "Blog Platform": ["blog", "blogging", "blogging platform"],
    "SaaS Application": ["saas", "software as a service", "subscription app"],
    "E-Commerce Store": ["store", "shop", "ecommerce", "e-commerce", "online store"],
    "Dashboard Application": ["dashboard", "admin panel", "analytics dashboard"],
    "Mobile Application": ["mobile app", "android app", "ios app", "phone app"],
    "API Service": ["api", "rest api", "backend service", "microservice"],
    "Data Pipeline": ["data pipeline", "etl", "data processing"],
    "ML Model": ["ml model", "machine learning model", "prediction model", "classifier"],
    "YouTube Channel": ["youtube channel", "youtube", "video channel"],
    "Podcast": ["podcast", "audio show"],
    "Marketing Campaign": ["marketing campaign", "ad campaign", "campaign"],
    "Brand Identity": ["brand", "branding", "brand identity", "logo"],
    "Game Project": ["game", "indie game", "mobile game", "video game"],
    "DevOps Pipeline": ["ci/cd", "cicd", "deployment pipeline", "devops"],
    "MVP Launch": ["mvp", "minimum viable product", "startup", "launch"],
    "Content Strategy": ["content strategy", "content plan", "content calendar"],
}


# ---------------------------------------------------------------------------
# DOMAIN DELIVERABLES
# Maps domain → list of deliverable dicts with title + description.
# The DeliverableDetector selects from these based on goal complexity.
# ---------------------------------------------------------------------------

DOMAIN_DELIVERABLES: dict[str, list[dict[str, str]]] = {
    "Web Development": [
        {"title": "Requirements Document", "description": "Define project scope, features, and technical requirements."},
        {"title": "UI/UX Design", "description": "Create wireframes, mockups, and a design system for the application."},
        {"title": "Frontend Development", "description": "Build the client-side interface using a modern framework."},
        {"title": "Backend Development", "description": "Implement server-side logic, APIs, and data models."},
        {"title": "Database Design", "description": "Design the data schema and set up the database."},
        {"title": "Authentication System", "description": "Implement user registration, login, and session management."},
        {"title": "Testing & QA", "description": "Write unit tests, integration tests, and perform quality assurance."},
        {"title": "Deployment & Hosting", "description": "Deploy the application to production and configure hosting."},
    ],
    "Mobile Development": [
        {"title": "App Requirements", "description": "Define features, platform targets, and user stories."},
        {"title": "UI/UX Design", "description": "Design mobile-optimized screens, flows, and interactions."},
        {"title": "App Architecture", "description": "Set up project structure, navigation, and state management."},
        {"title": "Core Feature Development", "description": "Build the primary features and screens of the application."},
        {"title": "API Integration", "description": "Connect the app to backend services and external APIs."},
        {"title": "Testing & Debugging", "description": "Test on devices, fix bugs, and optimize performance."},
        {"title": "App Store Submission", "description": "Prepare assets, write descriptions, and submit to app stores."},
    ],
    "Data Science": [
        {"title": "Problem Definition", "description": "Define the analytical question, success metrics, and scope."},
        {"title": "Data Collection", "description": "Gather, source, and import relevant datasets."},
        {"title": "Data Cleaning & EDA", "description": "Clean data, handle missing values, and perform exploratory analysis."},
        {"title": "Feature Engineering", "description": "Create and select features that improve model performance."},
        {"title": "Model Development", "description": "Train, evaluate, and tune machine learning models."},
        {"title": "Model Validation", "description": "Validate model performance using cross-validation and test sets."},
        {"title": "Results Presentation", "description": "Create visualizations, reports, and documentation of findings."},
        {"title": "Deployment", "description": "Deploy the model as an API or integrate into a production system."},
    ],
    "Content Creation": [
        {"title": "Content Strategy", "description": "Define target audience, content pillars, and publishing schedule."},
        {"title": "Channel/Platform Setup", "description": "Create and optimize profiles on target platforms."},
        {"title": "Content Production", "description": "Record, film, or write the initial batch of content."},
        {"title": "Editing & Post-Production", "description": "Edit content, add graphics, music, and final touches."},
        {"title": "Branding & Thumbnails", "description": "Create consistent visual branding, thumbnails, and graphics."},
        {"title": "Publishing & Distribution", "description": "Publish content and distribute across platforms."},
        {"title": "Analytics & Optimization", "description": "Track performance metrics and optimize content strategy."},
    ],
    "Marketing": [
        {"title": "Market Research", "description": "Analyze target market, competitors, and customer personas."},
        {"title": "Marketing Strategy", "description": "Define channels, messaging, budget, and campaign goals."},
        {"title": "Content Creation", "description": "Produce marketing copy, visuals, and campaign assets."},
        {"title": "Campaign Setup", "description": "Configure ad platforms, email sequences, and landing pages."},
        {"title": "Launch & Execution", "description": "Execute the campaign across all planned channels."},
        {"title": "Analytics & Reporting", "description": "Track KPIs, measure ROI, and generate performance reports."},
        {"title": "Optimization", "description": "A/B test, refine messaging, and improve conversion rates."},
    ],
    "Game Development": [
        {"title": "Game Design Document", "description": "Define game mechanics, story, art style, and technical scope."},
        {"title": "Art & Asset Creation", "description": "Create sprites, models, textures, and visual assets."},
        {"title": "Core Mechanics", "description": "Implement fundamental gameplay systems and physics."},
        {"title": "Level Design", "description": "Design and build game levels, environments, and progression."},
        {"title": "Audio & Sound", "description": "Create or source sound effects, music, and ambient audio."},
        {"title": "UI & Menus", "description": "Build menus, HUD elements, and in-game UI."},
        {"title": "Testing & Balancing", "description": "Playtest, fix bugs, and balance game difficulty."},
        {"title": "Publishing", "description": "Prepare builds and publish to target platforms."},
    ],
    "E-Commerce": [
        {"title": "Business Planning", "description": "Define products, pricing strategy, and business model."},
        {"title": "Store Design", "description": "Design the storefront, product pages, and checkout flow."},
        {"title": "Product Catalog", "description": "Set up product listings with descriptions, images, and categories."},
        {"title": "Payment Integration", "description": "Configure payment gateways, pricing, and tax settings."},
        {"title": "Shipping & Fulfillment", "description": "Set up shipping options, fulfillment workflows, and policies."},
        {"title": "Marketing & SEO", "description": "Optimize for search engines and set up initial marketing."},
        {"title": "Launch & Operations", "description": "Go live and establish order management processes."},
    ],
    "DevOps": [
        {"title": "Infrastructure Planning", "description": "Define architecture, cloud provider, and resource requirements."},
        {"title": "Environment Setup", "description": "Configure development, staging, and production environments."},
        {"title": "CI/CD Pipeline", "description": "Set up automated build, test, and deployment pipelines."},
        {"title": "Containerization", "description": "Dockerize applications and configure orchestration."},
        {"title": "Monitoring & Logging", "description": "Implement monitoring, alerting, and centralized logging."},
        {"title": "Security & Compliance", "description": "Configure security policies, secrets management, and compliance."},
        {"title": "Documentation", "description": "Document infrastructure, runbooks, and operational procedures."},
    ],
}

# Fallback for unrecognized domains
DOMAIN_DELIVERABLES["General"] = [
    {"title": "Project Planning", "description": "Define scope, objectives, and success criteria."},
    {"title": "Research & Discovery", "description": "Research best practices, tools, and approaches."},
    {"title": "Core Implementation", "description": "Build the primary deliverable of the project."},
    {"title": "Review & Refinement", "description": "Review work, gather feedback, and make improvements."},
    {"title": "Documentation", "description": "Document the project, processes, and outcomes."},
    {"title": "Delivery", "description": "Finalize and deliver the completed project."},
]


# ---------------------------------------------------------------------------
# DOMAIN TOOLS
# Maps domain → list of tool dicts with name, category, and reason.
# The ToolRecommender selects and deduplicates from these.
# ---------------------------------------------------------------------------

DOMAIN_TOOLS: dict[str, list[dict[str, str]]] = {
    "Web Development": [
        {"name": "VS Code", "category": "Development", "reason": "Industry-standard code editor with extensions for web development."},
        {"name": "Figma", "category": "Design", "reason": "Create wireframes, prototypes, and design systems collaboratively."},
        {"name": "React", "category": "Development", "reason": "Build interactive, component-based user interfaces."},
        {"name": "Node.js", "category": "Development", "reason": "JavaScript runtime for backend development and tooling."},
        {"name": "Tailwind CSS", "category": "Development", "reason": "Utility-first CSS framework for rapid styling."},
        {"name": "Git", "category": "Development", "reason": "Version control for tracking changes and collaboration."},
        {"name": "GitHub", "category": "Development", "reason": "Host repositories, manage issues, and automate workflows."},
        {"name": "Vercel", "category": "Development", "reason": "Deploy frontend applications with zero configuration."},
        {"name": "ChatGPT", "category": "AI", "reason": "Generate code snippets, debug issues, and brainstorm solutions."},
        {"name": "Postman", "category": "Development", "reason": "Test and document REST APIs during development."},
    ],
    "Mobile Development": [
        {"name": "VS Code", "category": "Development", "reason": "Lightweight editor with extensions for mobile development."},
        {"name": "Android Studio", "category": "Development", "reason": "Official IDE for Android development with built-in emulator."},
        {"name": "Xcode", "category": "Development", "reason": "Apple's IDE for iOS development and App Store submissions."},
        {"name": "Flutter", "category": "Development", "reason": "Build cross-platform mobile apps from a single codebase."},
        {"name": "Figma", "category": "Design", "reason": "Design mobile UI screens and prototypes."},
        {"name": "Firebase", "category": "Development", "reason": "Backend services: authentication, database, and hosting."},
        {"name": "Git", "category": "Development", "reason": "Version control for tracking changes and collaboration."},
        {"name": "ChatGPT", "category": "AI", "reason": "Generate code, debug issues, and learn new frameworks."},
        {"name": "TestFlight", "category": "Development", "reason": "Beta testing for iOS applications before App Store release."},
    ],
    "Data Science": [
        {"name": "Python", "category": "Development", "reason": "Primary language for data science and machine learning."},
        {"name": "Jupyter Notebook", "category": "Development", "reason": "Interactive environment for data exploration and visualization."},
        {"name": "Pandas", "category": "Development", "reason": "Data manipulation and analysis library."},
        {"name": "Scikit-learn", "category": "Development", "reason": "Machine learning library with standard algorithms."},
        {"name": "TensorFlow", "category": "Development", "reason": "Deep learning framework for building neural networks."},
        {"name": "Matplotlib", "category": "Development", "reason": "Create static, animated, and interactive visualizations."},
        {"name": "Kaggle", "category": "Development", "reason": "Access datasets, competitions, and community notebooks."},
        {"name": "ChatGPT", "category": "AI", "reason": "Explain algorithms, debug code, and brainstorm approaches."},
        {"name": "Google Colab", "category": "Development", "reason": "Free cloud-based Jupyter notebooks with GPU support."},
        {"name": "Git", "category": "Development", "reason": "Version control for tracking experiments and collaboration."},
    ],
    "Content Creation": [
        {"name": "Canva", "category": "Design", "reason": "Create thumbnails, graphics, and social media visuals."},
        {"name": "Adobe Premiere Pro", "category": "Design", "reason": "Professional video editing software."},
        {"name": "DaVinci Resolve", "category": "Design", "reason": "Free professional-grade video editing and color grading."},
        {"name": "OBS Studio", "category": "Productivity", "reason": "Free screen recording and live streaming software."},
        {"name": "ChatGPT", "category": "AI", "reason": "Generate scripts, content ideas, and social media copy."},
        {"name": "Notion", "category": "Productivity", "reason": "Plan content calendars and organize project notes."},
        {"name": "YouTube Studio", "category": "Productivity", "reason": "Upload, manage, and analyze YouTube content."},
        {"name": "Audacity", "category": "Productivity", "reason": "Free audio recording and editing for podcasts."},
    ],
    "Marketing": [
        {"name": "Google Analytics", "category": "Marketing", "reason": "Track website traffic, conversions, and user behavior."},
        {"name": "Mailchimp", "category": "Marketing", "reason": "Email marketing automation and campaign management."},
        {"name": "Canva", "category": "Design", "reason": "Design marketing assets, social posts, and ads."},
        {"name": "Google Ads", "category": "Marketing", "reason": "Run paid search and display advertising campaigns."},
        {"name": "SEMrush", "category": "Marketing", "reason": "SEO research, keyword tracking, and competitor analysis."},
        {"name": "Buffer", "category": "Marketing", "reason": "Schedule and manage social media posts across platforms."},
        {"name": "ChatGPT", "category": "AI", "reason": "Generate marketing copy, ad text, and email sequences."},
        {"name": "Notion", "category": "Productivity", "reason": "Plan campaigns, track tasks, and document strategies."},
        {"name": "Hotjar", "category": "Marketing", "reason": "Heatmaps and session recordings for UX insights."},
    ],
    "Game Development": [
        {"name": "Unity", "category": "Development", "reason": "Versatile game engine for 2D and 3D games."},
        {"name": "Unreal Engine", "category": "Development", "reason": "High-fidelity game engine for AAA-quality graphics."},
        {"name": "Godot", "category": "Development", "reason": "Free, open-source game engine with intuitive scripting."},
        {"name": "Aseprite", "category": "Design", "reason": "Pixel art editor for sprites and game assets."},
        {"name": "Blender", "category": "Design", "reason": "Free 3D modeling, animation, and rendering tool."},
        {"name": "FMOD", "category": "Development", "reason": "Audio middleware for interactive game sound."},
        {"name": "Git", "category": "Development", "reason": "Version control for game project collaboration."},
        {"name": "ChatGPT", "category": "AI", "reason": "Generate game logic, debug scripts, and brainstorm mechanics."},
        {"name": "Trello", "category": "Productivity", "reason": "Track game development tasks and milestones."},
    ],
    "E-Commerce": [
        {"name": "Shopify", "category": "Development", "reason": "All-in-one e-commerce platform for online stores."},
        {"name": "WooCommerce", "category": "Development", "reason": "WordPress-based e-commerce plugin for custom stores."},
        {"name": "Stripe", "category": "Development", "reason": "Payment processing API for online transactions."},
        {"name": "Canva", "category": "Design", "reason": "Create product images, banners, and marketing materials."},
        {"name": "Google Analytics", "category": "Marketing", "reason": "Track store traffic, conversions, and customer behavior."},
        {"name": "Mailchimp", "category": "Marketing", "reason": "Email marketing for customer retention and promotions."},
        {"name": "ChatGPT", "category": "AI", "reason": "Write product descriptions, SEO copy, and marketing emails."},
        {"name": "Figma", "category": "Design", "reason": "Design custom store layouts and product pages."},
    ],
    "DevOps": [
        {"name": "Docker", "category": "Development", "reason": "Containerize applications for consistent deployments."},
        {"name": "Kubernetes", "category": "Development", "reason": "Orchestrate containers at scale in production."},
        {"name": "Terraform", "category": "Development", "reason": "Infrastructure as code for cloud resource provisioning."},
        {"name": "GitHub Actions", "category": "Development", "reason": "Automate CI/CD pipelines directly from GitHub."},
        {"name": "AWS", "category": "Development", "reason": "Cloud platform for hosting, storage, and compute."},
        {"name": "Prometheus", "category": "Development", "reason": "Monitoring and alerting for infrastructure and applications."},
        {"name": "Grafana", "category": "Development", "reason": "Visualization dashboards for monitoring data."},
        {"name": "Ansible", "category": "Development", "reason": "Configuration management and automation tool."},
        {"name": "ChatGPT", "category": "AI", "reason": "Generate configs, debug infrastructure issues, and learn tools."},
    ],
}

DOMAIN_TOOLS["General"] = [
    {"name": "ChatGPT", "category": "AI", "reason": "General-purpose AI assistant for planning and brainstorming."},
    {"name": "Notion", "category": "Productivity", "reason": "All-in-one workspace for notes, tasks, and documentation."},
    {"name": "Google Docs", "category": "Productivity", "reason": "Collaborative document editing and sharing."},
    {"name": "Trello", "category": "Productivity", "reason": "Visual task management with boards and cards."},
    {"name": "Canva", "category": "Design", "reason": "Create visual assets and presentations easily."},
    {"name": "Git", "category": "Development", "reason": "Version control for tracking changes."},
]


# ---------------------------------------------------------------------------
# DOMAIN WORKFLOWS
# Maps domain → list of workflow step templates.
# Templates use {placeholders} that are interpolated by WorkflowGenerator.
# ---------------------------------------------------------------------------

DOMAIN_WORKFLOWS: dict[str, list[dict[str, str]]] = {
    "Web Development": [
        {
            "title": "Define Project Requirements",
            "tool": "Notion",
            "why": "Structured documentation for project scope and feature planning.",
            "what_to_do": "Create a project requirements document outlining features, tech stack, and timeline.",
            "expected_result": "A clear requirements document with defined scope and priorities.",
        },
        {
            "title": "Research Competitors & Inspiration",
            "tool": "ChatGPT",
            "why": "Quickly gather competitive analysis and design inspiration.",
            "what_to_do": "Research similar projects and identify best practices for your domain.",
            "expected_result": "A list of competitor insights and design inspiration references.",
        },
        {
            "title": "Design UI Mockups",
            "tool": "Figma",
            "why": "Industry-standard tool for creating interactive prototypes and design systems.",
            "what_to_do": "Create wireframes and high-fidelity mockups for all key pages.",
            "expected_result": "Complete UI mockups ready for development handoff.",
        },
        {
            "title": "Set Up Project Repository",
            "tool": "GitHub",
            "why": "Version control and collaboration platform for the codebase.",
            "what_to_do": "Initialize a Git repository, set up branching strategy, and create initial project structure.",
            "expected_result": "A configured repository with README, .gitignore, and folder structure.",
        },
        {
            "title": "Build Frontend Structure",
            "tool": "React",
            "why": "Component-based architecture for building interactive user interfaces.",
            "what_to_do": "Scaffold the frontend application, create routing, and build core components.",
            "expected_result": "A working frontend shell with navigation and placeholder pages.",
        },
        {
            "title": "Implement Backend API",
            "tool": "Node.js",
            "why": "JavaScript runtime for building fast, scalable server-side applications.",
            "what_to_do": "Build REST API endpoints, set up database connections, and implement business logic.",
            "expected_result": "Functional API endpoints with proper error handling and validation.",
        },
        {
            "title": "Connect Frontend to Backend",
            "tool": "VS Code",
            "why": "Full-featured editor for integrating frontend API calls with backend services.",
            "what_to_do": "Integrate API calls in the frontend, handle loading states, and display data.",
            "expected_result": "Frontend successfully fetching and displaying data from the backend.",
        },
        {
            "title": "Write Tests",
            "tool": "VS Code",
            "why": "Ensure code quality and catch regressions before deployment.",
            "what_to_do": "Write unit tests for critical components and integration tests for API endpoints.",
            "expected_result": "Test suite with passing tests covering core functionality.",
        },
        {
            "title": "Deploy to Production",
            "tool": "Vercel",
            "why": "Zero-configuration deployment platform optimized for frontend frameworks.",
            "what_to_do": "Configure deployment settings, connect repository, and deploy the application.",
            "expected_result": "Live application accessible via a public URL.",
        },
    ],
    "Mobile Development": [
        {
            "title": "Define App Requirements",
            "tool": "Notion",
            "why": "Organize features, user stories, and technical specifications.",
            "what_to_do": "Document app features, target platforms, and user stories.",
            "expected_result": "A structured requirements document for the mobile application.",
        },
        {
            "title": "Design Mobile UI",
            "tool": "Figma",
            "why": "Design mobile-optimized interfaces with proper touch targets and flows.",
            "what_to_do": "Create mobile screen designs, navigation flows, and component library.",
            "expected_result": "Complete mobile UI designs with interaction specifications.",
        },
        {
            "title": "Set Up Development Environment",
            "tool": "Android Studio",
            "why": "Official IDE with emulators and debugging tools for mobile development.",
            "what_to_do": "Install SDKs, configure emulators, and scaffold the project structure.",
            "expected_result": "Ready-to-develop environment with a running hello-world app.",
        },
        {
            "title": "Build Core Screens",
            "tool": "Flutter",
            "why": "Cross-platform framework for building native mobile apps from one codebase.",
            "what_to_do": "Implement the primary screens, navigation, and state management.",
            "expected_result": "Functional app with core screens and navigation working.",
        },
        {
            "title": "Integrate Backend Services",
            "tool": "Firebase",
            "why": "Pre-built backend services for auth, database, and cloud functions.",
            "what_to_do": "Connect the app to authentication, database, and any required APIs.",
            "expected_result": "App connected to backend with data flowing correctly.",
        },
        {
            "title": "Test on Devices",
            "tool": "TestFlight",
            "why": "Beta testing platform for distributing builds to testers.",
            "what_to_do": "Test on physical devices, fix bugs, and optimize performance.",
            "expected_result": "Stable app passing all test scenarios on target devices.",
        },
        {
            "title": "Submit to App Store",
            "tool": "Xcode",
            "why": "Required tool for building and submitting iOS applications.",
            "what_to_do": "Prepare screenshots, write descriptions, and submit for review.",
            "expected_result": "App submitted and approved on target app stores.",
        },
    ],
    "Data Science": [
        {
            "title": "Define the Problem",
            "tool": "Notion",
            "why": "Document the analytical question and success criteria clearly.",
            "what_to_do": "Write a problem statement, define success metrics, and outline the approach.",
            "expected_result": "A clear problem definition with measurable success criteria.",
        },
        {
            "title": "Collect & Load Data",
            "tool": "Python",
            "why": "Primary language for data ingestion with extensive library support.",
            "what_to_do": "Source datasets, load into dataframes, and verify data integrity.",
            "expected_result": "Raw datasets loaded and accessible for analysis.",
        },
        {
            "title": "Explore & Clean Data",
            "tool": "Jupyter Notebook",
            "why": "Interactive environment for iterative data exploration and visualization.",
            "what_to_do": "Perform EDA, handle missing values, remove duplicates, and normalize data.",
            "expected_result": "Clean dataset with documented data quality observations.",
        },
        {
            "title": "Engineer Features",
            "tool": "Pandas",
            "why": "Powerful data manipulation library for feature creation and transformation.",
            "what_to_do": "Create new features, encode categoricals, and select relevant variables.",
            "expected_result": "Feature matrix ready for model training.",
        },
        {
            "title": "Train Models",
            "tool": "Scikit-learn",
            "why": "Standard ML library with consistent API for training and evaluation.",
            "what_to_do": "Train multiple models, compare performance, and tune hyperparameters.",
            "expected_result": "Trained models with performance metrics documented.",
        },
        {
            "title": "Evaluate & Validate",
            "tool": "Matplotlib",
            "why": "Visualization library for plotting model performance and results.",
            "what_to_do": "Create confusion matrices, ROC curves, and performance comparison charts.",
            "expected_result": "Visual evaluation report with model comparison.",
        },
        {
            "title": "Present Results",
            "tool": "Google Colab",
            "why": "Shareable notebook format for presenting analysis and results.",
            "what_to_do": "Create a clean presentation notebook with findings and recommendations.",
            "expected_result": "Polished notebook ready for stakeholder review.",
        },
    ],
    "Content Creation": [
        {
            "title": "Define Content Strategy",
            "tool": "Notion",
            "why": "Organize content pillars, audience personas, and publishing schedule.",
            "what_to_do": "Define your niche, target audience, content pillars, and posting frequency.",
            "expected_result": "A documented content strategy with clear direction.",
        },
        {
            "title": "Set Up Platform Profiles",
            "tool": "Canva",
            "why": "Create professional profile banners, logos, and branding assets.",
            "what_to_do": "Design channel art, profile pictures, and branding templates.",
            "expected_result": "Fully branded profiles on target platforms.",
        },
        {
            "title": "Generate Content Ideas",
            "tool": "ChatGPT",
            "why": "AI-powered brainstorming for content topics and scripts.",
            "what_to_do": "Generate a list of content ideas, outlines, and potential titles.",
            "expected_result": "A content calendar with at least 10 planned pieces.",
        },
        {
            "title": "Produce Content",
            "tool": "OBS Studio",
            "why": "Free, powerful software for screen recording and live streaming.",
            "what_to_do": "Record or create your first batch of content pieces.",
            "expected_result": "Raw content files ready for editing.",
        },
        {
            "title": "Edit & Post-Produce",
            "tool": "DaVinci Resolve",
            "why": "Professional-grade free video editor with advanced features.",
            "what_to_do": "Edit footage, add graphics, music, transitions, and color grade.",
            "expected_result": "Polished content pieces ready for publishing.",
        },
        {
            "title": "Create Thumbnails & Graphics",
            "tool": "Canva",
            "why": "Quick creation of eye-catching thumbnails and social graphics.",
            "what_to_do": "Design thumbnails for each piece and social media promotional graphics.",
            "expected_result": "Attention-grabbing thumbnails and promotional materials.",
        },
        {
            "title": "Publish & Distribute",
            "tool": "YouTube Studio",
            "why": "Official platform for uploading, optimizing, and managing content.",
            "what_to_do": "Upload content, write descriptions, add tags, and schedule publishing.",
            "expected_result": "Content published and discoverable on target platforms.",
        },
    ],
    "Marketing": [
        {
            "title": "Research Target Market",
            "tool": "SEMrush",
            "why": "Comprehensive research tool for market analysis and competitor insights.",
            "what_to_do": "Analyze competitors, identify target keywords, and map the market landscape.",
            "expected_result": "Market research report with competitor analysis and keyword targets.",
        },
        {
            "title": "Define Marketing Strategy",
            "tool": "Notion",
            "why": "Structure campaign plans, timelines, and budget allocations.",
            "what_to_do": "Create a marketing plan with channels, messaging, budget, and KPIs.",
            "expected_result": "A comprehensive marketing strategy document.",
        },
        {
            "title": "Create Marketing Assets",
            "tool": "Canva",
            "why": "Quickly design professional marketing visuals and ad creatives.",
            "what_to_do": "Design ad creatives, social posts, email templates, and landing page mockups.",
            "expected_result": "A library of marketing assets ready for campaign use.",
        },
        {
            "title": "Write Marketing Copy",
            "tool": "ChatGPT",
            "why": "Generate persuasive copy variants for A/B testing.",
            "what_to_do": "Write ad copy, email sequences, landing page text, and social media posts.",
            "expected_result": "Multiple copy variants for each channel and campaign.",
        },
        {
            "title": "Set Up Campaigns",
            "tool": "Google Ads",
            "why": "Reach target audience through paid search and display advertising.",
            "what_to_do": "Configure campaign targeting, budgets, ad groups, and bidding strategies.",
            "expected_result": "Live ad campaigns configured and ready to launch.",
        },
        {
            "title": "Launch Email Marketing",
            "tool": "Mailchimp",
            "why": "Automate email sequences and manage subscriber lists.",
            "what_to_do": "Set up email templates, automation flows, and subscriber segments.",
            "expected_result": "Automated email campaigns running with welcome sequences.",
        },
        {
            "title": "Track & Optimize",
            "tool": "Google Analytics",
            "why": "Track campaign performance, conversions, and user behavior.",
            "what_to_do": "Set up tracking, monitor KPIs, and create performance dashboards.",
            "expected_result": "Analytics dashboard showing campaign performance metrics.",
        },
    ],
    "Game Development": [
        {
            "title": "Write Game Design Document",
            "tool": "Notion",
            "why": "Structured documentation for game mechanics, story, and scope.",
            "what_to_do": "Document game concept, mechanics, art style, target platform, and scope.",
            "expected_result": "Complete game design document with all specifications.",
        },
        {
            "title": "Create Art Assets",
            "tool": "Aseprite",
            "why": "Dedicated pixel art editor for game sprites and animations.",
            "what_to_do": "Create character sprites, environment tiles, UI elements, and animations.",
            "expected_result": "Complete set of art assets for the game prototype.",
        },
        {
            "title": "Set Up Game Engine Project",
            "tool": "Unity",
            "why": "Versatile engine supporting 2D and 3D with large community and asset store.",
            "what_to_do": "Create project, configure settings, import assets, and set up scene structure.",
            "expected_result": "Game project scaffolded with assets imported and scene ready.",
        },
        {
            "title": "Implement Core Mechanics",
            "tool": "Unity",
            "why": "Built-in physics, input handling, and scripting for game logic.",
            "what_to_do": "Code player movement, interactions, game rules, and core systems.",
            "expected_result": "Playable prototype with core mechanics functioning.",
        },
        {
            "title": "Design & Build Levels",
            "tool": "Unity",
            "why": "Scene editor and tilemap tools for efficient level creation.",
            "what_to_do": "Design level layouts, place objects, and configure progression.",
            "expected_result": "At least one complete, playable level.",
        },
        {
            "title": "Add Audio",
            "tool": "FMOD",
            "why": "Audio middleware for dynamic, interactive game sound.",
            "what_to_do": "Integrate sound effects, background music, and ambient audio.",
            "expected_result": "Game with complete audio design enhancing the experience.",
        },
        {
            "title": "Build UI & Menus",
            "tool": "Unity",
            "why": "Built-in UI system for menus, HUD, and in-game interfaces.",
            "what_to_do": "Create main menu, pause menu, HUD, and settings screens.",
            "expected_result": "Complete UI system with all menus functional.",
        },
        {
            "title": "Playtest & Polish",
            "tool": "Trello",
            "why": "Track bugs, feedback, and polish tasks during playtesting.",
            "what_to_do": "Conduct playtests, document bugs, fix issues, and balance difficulty.",
            "expected_result": "Polished game ready for release.",
        },
    ],
    "E-Commerce": [
        {
            "title": "Plan Business Model",
            "tool": "Notion",
            "why": "Structure business planning, pricing, and product strategy.",
            "what_to_do": "Define products, pricing, target market, and business model.",
            "expected_result": "Business plan document with clear product and pricing strategy.",
        },
        {
            "title": "Set Up Online Store",
            "tool": "Shopify",
            "why": "Complete e-commerce platform with built-in hosting and payment processing.",
            "what_to_do": "Create store, choose theme, configure settings, and set up pages.",
            "expected_result": "Functional store with homepage, about page, and contact info.",
        },
        {
            "title": "Add Products",
            "tool": "Shopify",
            "why": "Built-in product management with variants, images, and inventory tracking.",
            "what_to_do": "Add product listings with descriptions, images, prices, and categories.",
            "expected_result": "Complete product catalog with organized categories.",
        },
        {
            "title": "Configure Payments",
            "tool": "Stripe",
            "why": "Reliable payment processing with support for multiple payment methods.",
            "what_to_do": "Set up payment gateway, configure tax settings, and test transactions.",
            "expected_result": "Working payment system with successful test transactions.",
        },
        {
            "title": "Design Store Branding",
            "tool": "Canva",
            "why": "Create professional product images and marketing materials.",
            "what_to_do": "Design logo, product images, banners, and email templates.",
            "expected_result": "Consistent brand identity across all store assets.",
        },
        {
            "title": "Set Up Marketing",
            "tool": "Mailchimp",
            "why": "Automate customer communications and promotional campaigns.",
            "what_to_do": "Create welcome emails, abandoned cart flows, and promotional campaigns.",
            "expected_result": "Automated email marketing system driving customer engagement.",
        },
        {
            "title": "Launch Store",
            "tool": "Google Analytics",
            "why": "Track store performance, traffic sources, and conversion rates.",
            "what_to_do": "Go live, set up tracking, and begin initial marketing push.",
            "expected_result": "Live store with analytics tracking and first visitors.",
        },
    ],
    "DevOps": [
        {
            "title": "Plan Infrastructure",
            "tool": "Notion",
            "why": "Document architecture decisions, resource requirements, and cost estimates.",
            "what_to_do": "Design system architecture, choose cloud provider, and plan resource allocation.",
            "expected_result": "Infrastructure architecture document with diagrams.",
        },
        {
            "title": "Provision Cloud Resources",
            "tool": "Terraform",
            "why": "Infrastructure as code for reproducible, version-controlled deployments.",
            "what_to_do": "Write Terraform configs for compute, networking, storage, and databases.",
            "expected_result": "Cloud infrastructure provisioned and accessible.",
        },
        {
            "title": "Containerize Applications",
            "tool": "Docker",
            "why": "Consistent, portable application packaging across environments.",
            "what_to_do": "Create Dockerfiles, build images, and configure docker-compose for local dev.",
            "expected_result": "Applications running in containers locally and in CI.",
        },
        {
            "title": "Set Up CI/CD Pipeline",
            "tool": "GitHub Actions",
            "why": "Native CI/CD integration with GitHub repositories.",
            "what_to_do": "Create workflow files for building, testing, and deploying on push/PR.",
            "expected_result": "Automated pipeline that builds, tests, and deploys on every commit.",
        },
        {
            "title": "Configure Orchestration",
            "tool": "Kubernetes",
            "why": "Production-grade container orchestration with scaling and self-healing.",
            "what_to_do": "Create deployment manifests, services, and ingress configurations.",
            "expected_result": "Applications deployed and managed in a Kubernetes cluster.",
        },
        {
            "title": "Set Up Monitoring",
            "tool": "Prometheus",
            "why": "Industry-standard monitoring with powerful alerting capabilities.",
            "what_to_do": "Configure metrics collection, create alert rules, and set up dashboards.",
            "expected_result": "Monitoring system with alerts for critical metrics.",
        },
        {
            "title": "Create Dashboards",
            "tool": "Grafana",
            "why": "Beautiful, customizable dashboards for visualizing infrastructure metrics.",
            "what_to_do": "Build dashboards for application performance, infrastructure health, and logs.",
            "expected_result": "Operational dashboards accessible to the team.",
        },
    ],
}

DOMAIN_WORKFLOWS["General"] = [
    {
        "title": "Define Project Scope",
        "tool": "Notion",
        "why": "Organize ideas, requirements, and plans in a structured workspace.",
        "what_to_do": "Write down your project objectives, scope, and success criteria.",
        "expected_result": "A clear project scope document.",
    },
    {
        "title": "Research Best Practices",
        "tool": "ChatGPT",
        "why": "Quickly research approaches, tools, and strategies for your project.",
        "what_to_do": "Research how others have accomplished similar goals and identify best practices.",
        "expected_result": "A summary of recommended approaches and key considerations.",
    },
    {
        "title": "Create Action Plan",
        "tool": "Trello",
        "why": "Visual task management for breaking work into actionable items.",
        "what_to_do": "Break the project into tasks, set priorities, and create a timeline.",
        "expected_result": "An organized task board with prioritized action items.",
    },
    {
        "title": "Execute Core Work",
        "tool": "Google Docs",
        "why": "Collaborative document creation for project deliverables.",
        "what_to_do": "Complete the primary deliverables of your project.",
        "expected_result": "Core project deliverables completed.",
    },
    {
        "title": "Review & Finalize",
        "tool": "Notion",
        "why": "Centralized review of all project outputs and documentation.",
        "what_to_do": "Review all deliverables, gather feedback, and make final revisions.",
        "expected_result": "Finalized project ready for delivery.",
    },
]


# ---------------------------------------------------------------------------
# DOMAIN KNOWLEDGE AREAS
# Maps domain → knowledge areas by priority level.
# ---------------------------------------------------------------------------

DOMAIN_KNOWLEDGE: dict[str, dict[str, list[str]]] = {
    "Web Development": {
        "high": ["HTML", "CSS", "JavaScript", "Git", "Responsive Design"],
        "medium": ["React", "Node.js", "REST APIs", "TypeScript"],
        "low": ["SEO", "Web Accessibility", "Performance Optimization", "CI/CD"],
    },
    "Mobile Development": {
        "high": ["Mobile UI Patterns", "State Management", "Platform Guidelines"],
        "medium": ["Dart/Flutter", "React Native", "API Integration"],
        "low": ["App Store Optimization", "Push Notifications", "Analytics"],
    },
    "Data Science": {
        "high": ["Python", "Statistics", "Data Wrangling", "SQL"],
        "medium": ["Machine Learning Algorithms", "Data Visualization", "Feature Engineering"],
        "low": ["Deep Learning", "MLOps", "Big Data Tools", "Cloud Computing"],
    },
    "Content Creation": {
        "high": ["Content Strategy", "Video Editing", "Storytelling"],
        "medium": ["SEO", "Graphic Design", "Audio Production"],
        "low": ["Analytics", "Monetization", "Community Management"],
    },
    "Marketing": {
        "high": ["Digital Marketing", "Copywriting", "Analytics"],
        "medium": ["SEO", "Social Media Marketing", "Email Marketing"],
        "low": ["PPC Advertising", "Marketing Automation", "CRM"],
    },
    "Game Development": {
        "high": ["Game Design", "Programming Logic", "Game Engine Basics"],
        "medium": ["2D/3D Art", "Physics Simulation", "UI Design"],
        "low": ["Audio Design", "Multiplayer Networking", "Game Monetization"],
    },
    "E-Commerce": {
        "high": ["E-Commerce Platforms", "Product Photography", "Pricing Strategy"],
        "medium": ["Payment Processing", "Inventory Management", "Email Marketing"],
        "low": ["Supply Chain", "International Shipping", "Accounting"],
    },
    "DevOps": {
        "high": ["Linux", "Networking", "Docker", "CI/CD"],
        "medium": ["Cloud Platforms (AWS/GCP/Azure)", "Kubernetes", "Monitoring"],
        "low": ["Security", "Infrastructure as Code", "Cost Optimization"],
    },
}

DOMAIN_KNOWLEDGE["General"] = {
    "high": ["Project Management", "Communication", "Research Skills"],
    "medium": ["Time Management", "Documentation", "Problem Solving"],
    "low": ["Presentation Skills", "Collaboration Tools", "Risk Assessment"],
}


# ---------------------------------------------------------------------------
# DOMAIN ALTERNATIVES
# Maps domain → alternative workflow strategies.
# ---------------------------------------------------------------------------

DOMAIN_ALTERNATIVES: dict[str, dict[str, dict[str, object]]] = {
    "Web Development": {
        "fastest": {
            "summary": "Use AI-assisted builders and pre-built templates for rapid deployment.",
            "tools": ["Lovable", "Vercel", "ChatGPT", "Tailwind UI"],
        },
        "cheapest": {
            "summary": "Use entirely free and open-source tools with free hosting.",
            "tools": ["VS Code", "React", "GitHub Pages", "Canva Free"],
        },
        "highest_quality": {
            "summary": "Use professional design tools and enterprise-grade infrastructure.",
            "tools": ["Figma", "React", "AWS", "Sentry", "Datadog"],
        },
        "beginner_friendly": {
            "summary": "Use no-code/low-code platforms with visual editors.",
            "tools": ["WordPress", "Elementor", "Canva", "ChatGPT"],
        },
    },
    "Mobile Development": {
        "fastest": {
            "summary": "Use cross-platform frameworks with pre-built UI libraries.",
            "tools": ["Flutter", "Firebase", "Expo", "ChatGPT"],
        },
        "cheapest": {
            "summary": "Use free frameworks and open-source backend services.",
            "tools": ["React Native", "Supabase", "GitHub", "VS Code"],
        },
        "highest_quality": {
            "summary": "Build native apps with platform-specific optimizations.",
            "tools": ["Swift", "Kotlin", "Xcode", "Android Studio", "Firebase"],
        },
        "beginner_friendly": {
            "summary": "Use visual app builders with drag-and-drop interfaces.",
            "tools": ["FlutterFlow", "Adalo", "Firebase", "ChatGPT"],
        },
    },
    "Data Science": {
        "fastest": {
            "summary": "Use AutoML and pre-built models for rapid prototyping.",
            "tools": ["Google AutoML", "Google Colab", "ChatGPT", "Kaggle"],
        },
        "cheapest": {
            "summary": "Use free tools and cloud notebooks with open datasets.",
            "tools": ["Python", "Google Colab", "Kaggle", "Scikit-learn"],
        },
        "highest_quality": {
            "summary": "Use advanced frameworks with rigorous validation methodology.",
            "tools": ["PyTorch", "MLflow", "Weights & Biases", "AWS SageMaker"],
        },
        "beginner_friendly": {
            "summary": "Use visual tools and guided notebooks for learning.",
            "tools": ["Google Colab", "Kaggle Learn", "ChatGPT", "Orange"],
        },
    },
    "Content Creation": {
        "fastest": {
            "summary": "Use AI tools to generate scripts and automate editing.",
            "tools": ["ChatGPT", "Descript", "Canva", "Buffer"],
        },
        "cheapest": {
            "summary": "Use entirely free tools for creation and distribution.",
            "tools": ["OBS Studio", "DaVinci Resolve", "Canva Free", "Audacity"],
        },
        "highest_quality": {
            "summary": "Use professional production tools and premium assets.",
            "tools": ["Adobe Premiere Pro", "After Effects", "Epidemic Sound", "Adobe Photoshop"],
        },
        "beginner_friendly": {
            "summary": "Use simple, intuitive tools with templates.",
            "tools": ["Canva", "CapCut", "ChatGPT", "Anchor"],
        },
    },
    "Marketing": {
        "fastest": {
            "summary": "Use AI-generated copy and automated campaign tools.",
            "tools": ["ChatGPT", "Jasper", "Mailchimp", "Buffer"],
        },
        "cheapest": {
            "summary": "Use free marketing tools and organic growth strategies.",
            "tools": ["Google Search Console", "Canva Free", "Mailchimp Free", "Buffer Free"],
        },
        "highest_quality": {
            "summary": "Use enterprise marketing platforms with deep analytics.",
            "tools": ["HubSpot", "SEMrush", "Google Ads", "Salesforce"],
        },
        "beginner_friendly": {
            "summary": "Use all-in-one platforms with guided setup wizards.",
            "tools": ["Mailchimp", "Canva", "ChatGPT", "Google Analytics"],
        },
    },
    "Game Development": {
        "fastest": {
            "summary": "Use game templates and asset packs for rapid prototyping.",
            "tools": ["Unity Asset Store", "Unity", "ChatGPT", "Canva"],
        },
        "cheapest": {
            "summary": "Use free engines and open-source asset libraries.",
            "tools": ["Godot", "GIMP", "Audacity", "OpenGameArt"],
        },
        "highest_quality": {
            "summary": "Use industry-standard engines and professional tools.",
            "tools": ["Unreal Engine", "Blender", "Substance Painter", "FMOD"],
        },
        "beginner_friendly": {
            "summary": "Use visual scripting and beginner-oriented engines.",
            "tools": ["Godot", "Scratch", "Piskel", "ChatGPT"],
        },
    },
    "E-Commerce": {
        "fastest": {
            "summary": "Use all-in-one platforms with instant store setup.",
            "tools": ["Shopify", "Stripe", "Canva", "Mailchimp"],
        },
        "cheapest": {
            "summary": "Use free/open-source platforms with minimal overhead.",
            "tools": ["WooCommerce", "WordPress", "PayPal", "Canva Free"],
        },
        "highest_quality": {
            "summary": "Use custom development with enterprise commerce solutions.",
            "tools": ["Next.js Commerce", "Stripe", "Algolia", "Contentful"],
        },
        "beginner_friendly": {
            "summary": "Use guided store builders with templates.",
            "tools": ["Shopify", "Canva", "ChatGPT", "Google Analytics"],
        },
    },
    "DevOps": {
        "fastest": {
            "summary": "Use managed services and platform-as-a-service solutions.",
            "tools": ["Vercel", "Railway", "GitHub Actions", "Supabase"],
        },
        "cheapest": {
            "summary": "Use free-tier cloud services and open-source tools.",
            "tools": ["Docker", "GitHub Actions", "Oracle Cloud Free", "Grafana"],
        },
        "highest_quality": {
            "summary": "Use enterprise-grade infrastructure with full observability.",
            "tools": ["AWS", "Kubernetes", "Terraform", "Datadog", "PagerDuty"],
        },
        "beginner_friendly": {
            "summary": "Use simplified deployment platforms with minimal configuration.",
            "tools": ["Render", "Railway", "GitHub Actions", "ChatGPT"],
        },
    },
}

DOMAIN_ALTERNATIVES["General"] = {
    "fastest": {
        "summary": "Use AI assistants and automation to accelerate execution.",
        "tools": ["ChatGPT", "Notion AI", "Zapier"],
    },
    "cheapest": {
        "summary": "Use only free tools and platforms.",
        "tools": ["Google Docs", "Trello", "Canva Free", "ChatGPT"],
    },
    "highest_quality": {
        "summary": "Use professional tools with thorough review processes.",
        "tools": ["Notion", "Figma", "Slack", "Asana"],
    },
    "beginner_friendly": {
        "summary": "Use intuitive tools with templates and guided workflows.",
        "tools": ["Notion", "Canva", "ChatGPT", "Trello"],
    },
}


# ---------------------------------------------------------------------------
# COMPLEXITY RULES
# Heuristic helpers used by GoalAnalyzer to estimate complexity.
# ---------------------------------------------------------------------------

# Keywords that suggest higher complexity
HIGH_COMPLEXITY_KEYWORDS: list[str] = [
    "enterprise", "scalable", "microservices", "distributed",
    "real-time", "multiplayer", "machine learning", "deep learning",
    "blockchain", "security", "authentication", "payment",
    "production", "large-scale", "high-performance", "saas",
    "marketplace", "platform", "multi-tenant", "startup",
]

LOW_COMPLEXITY_KEYWORDS: list[str] = [
    "simple", "basic", "personal", "portfolio", "landing page",
    "static", "single page", "prototype", "demo", "tutorial",
    "beginner", "learn", "practice", "hobby",
]


# ---------------------------------------------------------------------------
# TIME ESTIMATES
# Maps (complexity, deliverable_count_bucket) → estimated time string.
# Buckets: "few" (1-3), "moderate" (4-6), "many" (7+)
# ---------------------------------------------------------------------------

TIME_ESTIMATES: dict[str, dict[str, str]] = {
    "Low": {
        "few": "2-4 hours",
        "moderate": "4-8 hours",
        "many": "1-2 days",
    },
    "Medium": {
        "few": "4-8 hours",
        "moderate": "1-3 days",
        "many": "3-5 days",
    },
    "High": {
        "few": "1-2 days",
        "moderate": "3-7 days",
        "many": "1-3 weeks",
    },
}
