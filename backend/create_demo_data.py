# demo_setup.py - Run this to setup complete demo data
# Usage: Get-Content create_demo_data.py | python manage.py shell

import os
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import (
    Campaign, AdContent, ImageAsset, Comment,
    DailyAnalytics, CampaignAnalyticsSummary,
    UserAPIKey, ABTest, ABTestVariation
)

User = get_user_model()

print("🎬 Setting up AdVision Demo Environment...")
print("=" * 60)

# ============================================================================
# 1. CREATE DEMO USERS
# ============================================================================
print("\n👤 Creating demo users...")

demo_users = [
    {'email': 'demo@advision.com', 'password': 'demo123', 'role': 'admin'},
    {'email': 'admin@advision.com', 'password': 'admin123', 'role': 'admin'},
    {'email': 'test@advision.com', 'password': 'test123', 'role': 'editor'},
]

for user_data in demo_users:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={'role': user_data['role']}
    )
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f"✅ Created user: {user_data['email']} / {user_data['password']}")
    else:
        print(f"ℹ️  User exists: {user_data['email']}")

# Use first user for demo data
demo_user = User.objects.get(email='demo@advision.com')

# ============================================================================
# 2. CREATE MOCK API KEYS (Auto-verified)
# ============================================================================
print("\n🔑 Creating mock API keys...")

api_keys_data = [
    {
        'api_type': 'google_ads',
        'api_name': 'My Google Ads Account',
        'account_id': 'demo-google-ads-123',
        'developer_token': 'demo-dev-token-xxx'
    },
    {
        'api_type': 'facebook_ads',
        'api_name': 'Main Facebook Business',
        'account_id': 'act_demo_456'
    },
    {
        'api_type': 'instagram_ads',
        'api_name': 'Instagram Business Account',
        'account_id': 'ig_demo_789'
    }
]

for key_data in api_keys_data:
    api_key, created = UserAPIKey.objects.get_or_create(
        user=demo_user,
        api_type=key_data['api_type'],
        api_name=key_data['api_name'],
        defaults={
            'account_id': key_data['account_id'],
            'developer_token': key_data.get('developer_token', ''),
            'verification_status': 'verified',
            'is_active': True,
            'last_verified': datetime.now()
        }
    )
    
    if created:
        # Encrypt a demo key
        api_key.encrypt_key(f'demo_{key_data["api_type"]}_key_12345')
        if key_data['api_type'] in ['facebook_ads', 'instagram_ads']:
            api_key.encrypt_secret(f'demo_{key_data["api_type"]}_secret_67890')
        api_key.save()
        print(f"✅ Created API key: {key_data['api_name']} (verified)")
    else:
        print(f"ℹ️  API key exists: {key_data['api_name']}")

# ============================================================================
# 3. CREATE DEMO CAMPAIGNS
# ============================================================================
print("\n📊 Creating demo campaigns...")

campaigns_data = [
    {
        'title': 'Summer Sale 2024 - Fashion Collection',
        'description': 'Promote our summer fashion collection with 30% discount across all platforms',
        'platform': 'instagram',
        'budget': 5000,
        'days_ago': 30
    },
    {
        'title': 'New Product Launch - Eco Water Bottles',
        'description': 'Launch our revolutionary eco-friendly stainless steel water bottles',
        'platform': 'facebook',
        'budget': 8000,
        'days_ago': 25
    },
    {
        'title': 'Brand Awareness - Millennial Targeting',
        'description': 'Increase brand visibility among millennials aged 25-35',
        'platform': 'youtube',
        'budget': 10000,
        'days_ago': 20
    },
    {
        'title': 'Holiday Special - Black Friday Deals',
        'description': 'Black Friday early access deals and promotions',
        'platform': 'tiktok',
        'budget': 6000,
        'days_ago': 15
    },
    {
        'title': 'LinkedIn B2B Campaign',
        'description': 'Target business professionals for enterprise solutions',
        'platform': 'linkedin',
        'budget': 7500,
        'days_ago': 10
    }
]

today = datetime.now().date()
campaigns = []

for camp_data in campaigns_data:
    start_date = today - timedelta(days=camp_data['days_ago'])
    end_date = today + timedelta(days=30)
    
    campaign, created = Campaign.objects.get_or_create(
        user=demo_user,
        title=camp_data['title'],
        defaults={
            'description': camp_data['description'],
            'platform': camp_data['platform'],
            'budget': camp_data['budget'],
            'start_date': start_date,
            'end_date': end_date,
            'is_active': True
        }
    )
    
    campaigns.append(campaign)
    
    if created:
        print(f"✅ Created campaign: {camp_data['title']}")
    else:
        print(f"ℹ️  Campaign exists: {camp_data['title']}")

# ============================================================================
# 4. CREATE DEMO AD CONTENT
# ============================================================================
print("\n✍️  Creating demo ad content...")

ad_content_templates = {
    'instagram': [
        "🌊 Dive into Summer Savings! Get 30% OFF on all beachwear. Limited time only! Shop now and make this summer unforgettable. #SummerSale #BeachReady",
        "Summer vibes only! 🏖️ Refresh your wardrobe with our hottest collection. Use code SUMMER30 at checkout. Link in bio! #FashionDeals",
        "☀️ Sun's out, deals are out! Exclusive summer sale - 30% OFF everything. Don't miss out! #ShopNow #SummerFashion"
    ],
    'facebook': [
        "Introducing the future of hydration 💧 Our new eco-friendly bottles keep drinks cold for 24hrs while saving the planet. Pre-order now!",
        "🌱 Sustainable. Stylish. Superior. Meet the water bottle that does it all. Join 50,000+ happy customers. Order yours today!",
        "Say goodbye to single-use plastics! Our premium stainless steel bottles are built to last a lifetime. Get 20% off launch special."
    ],
    'youtube': [
        "Join thousands who trust our brand. Premium quality. Affordable prices. Exceptional service. Discover the difference today.",
        "Why choose us? Award-winning products, 5-star customer service, and a community of 100,000+ satisfied customers. See for yourself.",
        "Transform your lifestyle with our innovative solutions. Watch real customer testimonials and start your journey today."
    ],
    'tiktok': [
        "🔥 Black Friday came early! Shop now before it's gone. Swipe up for exclusive deals you won't believe! #BlackFriday #Deals",
        "POV: You found the best Black Friday deals 😱 Limited stock! Act fast or cry later. Link in bio! #Shopping #Sales",
        "This Black Friday deal is INSANE! 🤯 Watch till the end. You'll thank me later! #BestDeals #MustHave"
    ],
    'linkedin': [
        "Empower your team with enterprise-grade solutions. Join Fortune 500 companies already transforming their business. Schedule a demo today.",
        "ROI that speaks for itself. Our clients see average productivity gains of 40% in the first quarter. Read the case studies.",
        "Professional tools for professional results. Trusted by industry leaders worldwide. Discover what sets us apart."
    ]
}

for campaign in campaigns:
    platform = campaign.platform
    templates = ad_content_templates.get(platform, ad_content_templates['facebook'])
    
    for i, text in enumerate(templates):
        tone = ['persuasive', 'witty', 'casual', 'formal'][i % 4]
        
        ad, created = AdContent.objects.get_or_create(
            campaign=campaign,
            text=text,
            defaults={
                'tone': tone,
                'platform': platform,
                'views': random.randint(10000, 50000),
                'clicks': random.randint(300, 2000),
                'conversions': random.randint(20, 150)
            }
        )
        
        if created:
            print(f"  ✅ Added ad for {campaign.title}")

# ============================================================================
# 5. GENERATE REALISTIC ANALYTICS DATA
# ============================================================================
print("\n📈 Generating realistic analytics data (30 days)...")

for campaign in campaigns:
    campaign_age = (today - campaign.start_date).days
    days_to_generate = min(30, campaign_age + 1)
    
    # Base metrics
    platform_multipliers = {
        'instagram': 500, 'facebook': 600, 'youtube': 800,
        'linkedin': 300, 'tiktok': 1000
    }
    
    base_impressions = platform_multipliers.get(campaign.platform, 500)
    daily_budget = float(campaign.budget) / max(days_to_generate, 1)
    
    for day_offset in range(days_to_generate):
        analytics_date = today - timedelta(days=days_to_generate - day_offset - 1)
        
        if analytics_date > today or analytics_date < campaign.start_date:
            continue
        
        # Growth pattern
        growth_factor = 1 + (day_offset / days_to_generate) * 0.5
        randomness = random.uniform(0.85, 1.15)
        
        impressions = int(base_impressions * growth_factor * randomness)
        ctr_rate = random.uniform(0.02, 0.05)
        clicks = int(impressions * ctr_rate)
        conversion_rate = random.uniform(0.05, 0.15)
        conversions = int(clicks * conversion_rate)
        spend = round(daily_budget * random.uniform(0.85, 1.15), 2)
        
        DailyAnalytics.objects.update_or_create(
            campaign=campaign,
            date=analytics_date,
            defaults={
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'spend': spend
            }
        )
    
    # Update summary
    summary, _ = CampaignAnalyticsSummary.objects.get_or_create(campaign=campaign)
    summary.update_metrics()
    
    print(f"  ✅ Generated analytics for {campaign.title}")
    print(f"     Total: {summary.total_impressions:,} impressions, {summary.total_clicks:,} clicks")

# ============================================================================
# 6. CREATE A/B TEST DEMO
# ============================================================================
print("\n🧪 Creating A/B test demos...")

# Create A/B test for first campaign
first_campaign = campaigns[0]
ab_test, created = ABTest.objects.get_or_create(
    campaign=first_campaign,
    name='Headline Test - Summer Sale',
    defaults={
        'description': 'Testing two different headlines to see which performs better',
        'status': 'running',
        'success_metric': 'ctr',
        'min_sample_size': 1000,
        'start_date': datetime.now() - timedelta(days=5)
    }
)

if created:
    # Create variations
    variation_a = ABTestVariation.objects.create(
        ab_test=ab_test,
        name='A',
        impressions=5000,
        clicks=250,
        conversions=25,
        spend=150
    )
    
    variation_b = ABTestVariation.objects.create(
        ab_test=ab_test,
        name='B',
        impressions=5000,
        clicks=320,
        conversions=35,
        spend=150
    )
    
    print(f"✅ Created A/B test: {ab_test.name}")
    print(f"   Variation A: {variation_a.ctr}% CTR")
    print(f"   Variation B: {variation_b.ctr}% CTR")

# ============================================================================
# 7. CREATE DEMO COMMENTS
# ============================================================================
print("\n💬 Adding team comments...")

comments_data = [
    "Great performance on this campaign! Let's increase the budget.",
    "The engagement rate is higher than expected. Good targeting!",
    "Can we A/B test different creatives next week?",
    "Excellent ROI on this one. Let's replicate the strategy.",
]

for i, campaign in enumerate(campaigns[:4]):
    comment, created = Comment.objects.get_or_create(
        campaign=campaign,
        user=demo_user,
        defaults={'message': comments_data[i]}
    )
    if created:
        print(f"  ✅ Added comment to {campaign.title}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("🎉 DEMO SETUP COMPLETE!")
print("=" * 60)
print("\n📋 DEMO CREDENTIALS:")
print("-" * 60)
for user_data in demo_users:
    print(f"Email: {user_data['email']}")
    print(f"Password: {user_data['password']}")
    print(f"Role: {user_data['role']}")
    print("-" * 60)

print("\n📊 DEMO DATA CREATED:")
print(f"✅ {len(campaigns)} Campaigns with realistic data")
print(f"✅ {AdContent.objects.filter(campaign__user=demo_user).count()} Ad Copy variations")
print(f"✅ {DailyAnalytics.objects.filter(campaign__user=demo_user).count()} Days of analytics")
print(f"✅ {UserAPIKey.objects.filter(user=demo_user).count()} API Keys (all verified)")
print(f"✅ {ABTest.objects.filter(campaign__user=demo_user).count()} A/B Tests")

print("\n🚀 READY TO DEMO!")
print("\n💡 FEATURES YOU CAN DEMONSTRATE:")
print("   1. Login with any demo account")
print("   2. View dashboard with real metrics")
print("   3. Browse campaigns with 30 days of data")
print("   4. View detailed analytics charts")
print("   5. Check API Keys page (all verified)")
print("   6. See A/B testing results")
print("   7. Generate AI content (requires API keys)")
print("   8. View audience insights")
print("   9. Check weekly reports")
print("   10. Sync campaigns (shows success messages)")

print("\n⚠️  NOTE: API keys are demo keys and won't connect to real platforms")
print("    But all features will work and show realistic data!")
print("\n🎬 Start your servers and begin the demo!")

# to delete the data
# Delete the database file
# rm db.sqlite3

# Recreate database
# python manage.py migrate

# Create your superuser
# python manage.py createsuperuser