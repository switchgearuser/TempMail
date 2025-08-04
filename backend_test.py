#!/usr/bin/env python3
"""
Backend API Testing for Temporary Email Service
Tests all endpoints with real Mail.tm API integration
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Get backend URL from frontend .env
BACKEND_URL = "https://c2492512-15e5-457b-ba95-4b0f68696007.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.created_inboxes = []  # Track created inboxes for cleanup
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def test_health_endpoint(self):
        """Test /api/health endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy" and "timestamp" in data:
                    self.log_test("Health Check", True, "Health endpoint returns healthy status", data)
                    return True
                else:
                    self.log_test("Health Check", False, f"Invalid health response structure", data)
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
            return False
    
    def test_domains_endpoint(self):
        """Test /api/domains endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/domains", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_test("Get Domains", True, f"Retrieved {len(data)} domains: {data}", data)
                    return True, data
                else:
                    self.log_test("Get Domains", False, f"Invalid domains response: expected non-empty list", data)
                    return False, None
            else:
                self.log_test("Get Domains", False, f"HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Get Domains", False, f"Request failed: {str(e)}")
            return False, None
    
    def test_create_inbox_no_params(self):
        """Test /api/inbox/create without parameters"""
        try:
            response = self.session.post(f"{API_BASE}/inbox/create", 
                                       json={}, 
                                       timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if self._validate_inbox_response(data):
                    inbox = data["inbox"]
                    self.created_inboxes.append(inbox)
                    self.log_test("Create Inbox (No Params)", True, 
                                f"Created inbox: {inbox['email']}, ID: {inbox['id']}", data)
                    return True, data
                else:
                    self.log_test("Create Inbox (No Params)", False, 
                                "Invalid response structure", data)
                    return False, None
            else:
                self.log_test("Create Inbox (No Params)", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Create Inbox (No Params)", False, f"Request failed: {str(e)}")
            return False, None
    
    def test_create_inbox_with_custom_name(self):
        """Test /api/inbox/create with custom_name parameter"""
        custom_name = f"testuser{int(time.time())}"
        
        try:
            response = self.session.post(f"{API_BASE}/inbox/create", 
                                       json={"custom_name": custom_name}, 
                                       timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if self._validate_inbox_response(data):
                    inbox = data["inbox"]
                    self.created_inboxes.append(inbox)
                    
                    # Check if custom name is used in email
                    email = inbox["email"]
                    if custom_name in email:
                        self.log_test("Create Inbox (Custom Name)", True, 
                                    f"Created inbox with custom name: {email}, ID: {inbox['id']}", data)
                        return True, data
                    else:
                        self.log_test("Create Inbox (Custom Name)", False, 
                                    f"Custom name '{custom_name}' not found in email '{email}'", data)
                        return False, None
                else:
                    self.log_test("Create Inbox (Custom Name)", False, 
                                "Invalid response structure", data)
                    return False, None
            else:
                self.log_test("Create Inbox (Custom Name)", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Create Inbox (Custom Name)", False, f"Request failed: {str(e)}")
            return False, None
    
    def test_get_messages(self, inbox_id: str, token: str):
        """Test /api/inbox/{inbox_id}/messages endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/inbox/{inbox_id}/messages", 
                                      params={"token": token}, 
                                      timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Get Messages", True, 
                                f"Retrieved {len(data)} messages for inbox {inbox_id}", data)
                    return True, data
                else:
                    self.log_test("Get Messages", False, 
                                f"Invalid response: expected list, got {type(data)}", data)
                    return False, None
            else:
                self.log_test("Get Messages", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Get Messages", False, f"Request failed: {str(e)}")
            return False, None
    
    def _validate_inbox_response(self, data: Dict[str, Any]) -> bool:
        """Validate inbox creation response structure"""
        try:
            # Check top-level structure
            if not isinstance(data, dict):
                return False
            
            required_fields = ["inbox", "messages", "message_count"]
            if not all(field in data for field in required_fields):
                return False
            
            # Check inbox structure
            inbox = data["inbox"]
            inbox_required_fields = ["id", "email", "domain", "password", "created_at"]
            if not all(field in inbox for field in inbox_required_fields):
                return False
            
            # Check that email contains @ and domain
            email = inbox["email"]
            domain = inbox["domain"]
            if "@" not in email or domain not in email:
                return False
            
            # Check messages is a list
            if not isinstance(data["messages"], list):
                return False
            
            # Check message_count is integer
            if not isinstance(data["message_count"], int):
                return False
            
            return True
            
        except Exception:
            return False
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("=" * 60)
        print("BACKEND API TESTING - TEMPORARY EMAIL SERVICE")
        print("=" * 60)
        print(f"Testing against: {API_BASE}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        # Test 1: Health check
        print("1. Testing Health Endpoint...")
        health_ok = self.test_health_endpoint()
        print()
        
        # Test 2: Get domains
        print("2. Testing Domains Endpoint...")
        domains_ok, domains = self.test_domains_endpoint()
        print()
        
        # Test 3: Create inbox without parameters
        print("3. Testing Create Inbox (No Parameters)...")
        inbox1_ok, inbox1_data = self.test_create_inbox_no_params()
        print()
        
        # Test 4: Create inbox with custom name
        print("4. Testing Create Inbox (Custom Name)...")
        inbox2_ok, inbox2_data = self.test_create_inbox_with_custom_name()
        print()
        
        # Test 5: Get messages for first inbox
        if inbox1_ok and inbox1_data:
            print("5. Testing Get Messages (First Inbox)...")
            inbox1 = inbox1_data["inbox"]
            messages1_ok, messages1 = self.test_get_messages(inbox1["id"], inbox1.get("token", ""))
            print()
        else:
            print("5. Skipping Get Messages (First Inbox) - inbox creation failed")
            messages1_ok = False
            print()
        
        # Test 6: Get messages for second inbox
        if inbox2_ok and inbox2_data:
            print("6. Testing Get Messages (Second Inbox)...")
            inbox2 = inbox2_data["inbox"]
            messages2_ok, messages2 = self.test_get_messages(inbox2["id"], inbox2.get("token", ""))
            print()
        else:
            print("6. Skipping Get Messages (Second Inbox) - inbox creation failed")
            messages2_ok = False
            print()
        
        # Summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 6
        passed_tests = sum([
            health_ok,
            domains_ok,
            inbox1_ok,
            inbox2_ok,
            messages1_ok,
            messages2_ok
        ])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Detailed results
        print("DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        print()
        print(f"Created {len(self.created_inboxes)} test inboxes:")
        for inbox in self.created_inboxes:
            print(f"  - {inbox['email']} (ID: {inbox['id']})")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Backend API is working correctly.")
        exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED! Check the details above.")
        exit(1)