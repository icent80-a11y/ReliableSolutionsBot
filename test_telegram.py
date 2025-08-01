#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from telegram.ext import Application
    print("✅ Telegram library imported successfully")
    print("🔍 Testing basic functionality...")
    
    # Test creating application instance without token
    print("📱 Creating application instance...")
    app = Application.builder().token("test_token").build()
    print("✅ Application created successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"⚠️ Other error: {e}")