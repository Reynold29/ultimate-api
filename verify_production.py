#!/usr/bin/env python3
"""
Production Verification Script
Tests the complete Ultimate Guitar Tab Parser API functionality
"""

import requests
import json
import time

def test_api_health():
    """Test if the API is running and healthy"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(process.env.VITE_API_URL, timeout=10)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False

def test_tab_parsing():
    """Test tab parsing with a real URL"""
    print("\n🎸 Testing Tab Parsing...")
    
    # Test URL that we know works
    test_url = "https://tabs.ultimate-guitar.com/tab/phil-wickham/what-an-awesome-god-chords-5749718"
    
    try:
        start_time = time.time()
        response = requests.get(
            "https://ultimate-api-production.up.railway.app/tab",
            params={"url": test_url},
            timeout=60
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify the response structure
            if 'blocks' in data and isinstance(data['blocks'], list):
                print(f"✅ Tab parsing successful in {response_time:.2f}s")
                print(f"📊 Found {len(data['blocks'])} blocks")
                
                # Check for lyrics and tabs
                has_lyrics = any('lyrics' in block for block in data['blocks'])
                has_tabs = any('tabs' in block for block in data['blocks'])
                
                if has_lyrics:
                    print("✅ Lyrics block found")
                if has_tabs:
                    print("✅ Tabs/chords block found")
                
                # Check for errors
                has_errors = any('error' in block for block in data['blocks'])
                if has_errors:
                    print("⚠️  Some blocks contain errors")
                    for block in data['blocks']:
                        if 'error' in block:
                            print(f"   Error: {block['error']}")
                
                return True
            else:
                print("❌ Invalid response format - missing 'blocks'")
                return False
        else:
            print(f"❌ API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Tab parsing failed: {e}")
        return False

def test_frontend():
    """Test if the frontend is accessible"""
    print("\n🌐 Testing Frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running on localhost:3000")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        return False

def main():
    """Run all production verification tests"""
    print("🚀 Ultimate Guitar Tab Parser - Production Verification")
    print("=" * 60)
    
    # Test API health
    api_healthy = test_api_health()
    
    # Test tab parsing
    parsing_working = test_tab_parsing()
    
    # Test frontend
    frontend_working = test_frontend()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 PRODUCTION VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"API Health:        {'✅ PASS' if api_healthy else '❌ FAIL'}")
    print(f"Tab Parsing:       {'✅ PASS' if parsing_working else '❌ FAIL'}")
    print(f"Frontend:          {'✅ PASS' if frontend_working else '❌ FAIL'}")
    
    if api_healthy and parsing_working and frontend_working:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("✅ API: http://ultimate-api-production.up.railway.app")
        print("✅ Frontend: http://localhost:3000")
        print("\nYou can now use the application!")
    else:
        print("\n⚠️  Some systems need attention")
        if not api_healthy:
            print("   - Start the API server: python3 run.py")
        if not frontend_working:
            print("   - Start the frontend: cd frontend && npm run dev")

if __name__ == "__main__":
    main() 