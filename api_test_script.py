#!/usr/bin/env python3
"""
Quick API Test Script for LMS Portal
This script tests basic API functionality before using Postman
"""

import requests
import json
import sys
from urllib.parse import urljoin

class LMSAPITester:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/') + '/'
        self.session = requests.Session()
        self.access_token = None
        
    def test_connection(self):
        """Test basic API connectivity"""
        print("🔗 Testing API connectivity...")
        try:
            response = self.session.get(urljoin(self.base_url, 'health/'))
            if response.status_code == 200:
                print("✅ API is responding")
                return True
            else:
                print(f"❌ API responded with status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to API. Is the server running?")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def test_endpoints_list(self):
        """Test API endpoints listing"""
        print("\n📋 Testing API endpoints listing...")
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                print("✅ API endpoints accessible")
                return True
            else:
                print(f"❌ Endpoints list failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error accessing endpoints: {e}")
            return False
    
    def test_login(self, username="admin", password="admin123"):
        """Test user authentication"""
        print(f"\n🔐 Testing login with username: {username}")
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = self.session.post(
                urljoin(self.base_url, 'auth/login/'),
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}'
                })
                print("✅ Login successful")
                
                # Print user info if available
                if 'user' in data:
                    user_info = data['user']
                    print(f"   User: {user_info.get('user', {}).get('first_name', 'N/A')} {user_info.get('user', {}).get('last_name', 'N/A')}")
                    print(f"   Role: {user_info.get('role_display', 'N/A')}")
                
                return True
            else:
                print(f"❌ Login failed with status {response.status_code}")
                if response.content:
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data}")
                    except:
                        print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def test_profile(self):
        """Test user profile access"""
        print("\n👤 Testing user profile access...")
        
        if not self.access_token:
            print("❌ No access token available. Login first.")
            return False
        
        try:
            response = self.session.get(urljoin(self.base_url, 'profile/me/'))
            
            if response.status_code == 200:
                print("✅ Profile access successful")
                data = response.json()
                if 'user' in data and 'username' in data['user']:
                    print(f"   Username: {data['user']['username']}")
                    print(f"   Role: {data.get('role_display', 'N/A')}")
                return True
            else:
                print(f"❌ Profile access failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Profile access error: {e}")
            return False
    
    def test_subjects_list(self):
        """Test subjects listing"""
        print("\n📚 Testing subjects listing...")
        
        if not self.access_token:
            print("❌ No access token available. Login first.")
            return False
        
        try:
            response = self.session.get(urljoin(self.base_url, 'subjects/'))
            
            if response.status_code == 200:
                data = response.json()
                subjects_count = len(data.get('results', []) if isinstance(data, dict) else data)
                print(f"✅ Subjects listing successful ({subjects_count} subjects)")
                return True
            elif response.status_code == 403:
                print("⚠️  Subjects access forbidden (check user permissions)")
                return True  # This might be expected for some roles
            else:
                print(f"❌ Subjects listing failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Subjects listing error: {e}")
            return False
    
    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        print("\n📊 Testing dashboard statistics...")
        
        if not self.access_token:
            print("❌ No access token available. Login first.")
            return False
        
        try:
            response = self.session.get(urljoin(self.base_url, 'dashboard/stats/'))
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Dashboard stats successful")
                # Print some stats if available
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, (int, str)):
                            print(f"   {key}: {value}")
                return True
            else:
                print(f"❌ Dashboard stats failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Dashboard stats error: {e}")
            return False
    
    def run_all_tests(self, username="admin", password="admin123"):
        """Run all basic tests"""
        print("🧪 Running LMS API Basic Tests")
        print("=" * 50)
        
        results = []
        
        # Test connection
        results.append(self.test_connection())
        
        # Test endpoints listing
        results.append(self.test_endpoints_list())
        
        # Test authentication
        results.append(self.test_login(username, password))
        
        # Test authenticated endpoints only if login succeeded
        if self.access_token:
            results.append(self.test_profile())
            results.append(self.test_subjects_list())
            results.append(self.test_dashboard_stats())
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 Test Summary")
        print("=" * 50)
        
        passed = sum(results)
        total = len(results)
        
        if passed == total:
            print(f"✅ All tests passed! ({passed}/{total})")
            print("\n🎉 Your API is ready for Postman testing!")
        else:
            print(f"⚠️  {passed}/{total} tests passed")
            print("\n🔧 Please check the failed tests before using Postman")
        
        return passed == total


def main():
    """Main function"""
    print("LMS Portal API Quick Test Script")
    print("================================\n")
    
    # Check command line arguments
    base_url = "http://localhost:8000/api"
    username = "admin"
    password = "admin123"
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    if len(sys.argv) > 2:
        username = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]
    
    print(f"Testing API at: {base_url}")
    print(f"Using credentials: {username} / {'*' * len(password)}")
    print()
    
    # Create tester and run tests
    tester = LMSAPITester(base_url)
    success = tester.run_all_tests(username, password)
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("- Ensure Django server is running: python manage.py runserver")
        print("- Check if database is migrated: python manage.py migrate")
        print("- Verify admin user exists: python manage.py createsuperuser")
        print("- Check firewall/network settings")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 