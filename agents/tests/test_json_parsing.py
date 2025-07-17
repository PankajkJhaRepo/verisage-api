                      
"""
Test script to verify the enhanced JSON parsing handles various formats
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_json_parsing():
    """Test the enhanced JSON parsing with various formats"""
    
    from agents.researcher.deep_researcher.chains.deep_research_chain import parse_agent_response
    
    test_response_4_backticks = {
        "output": '''````json
{
    "topics": [
        {
            "topic": "AI in Medical Science",
            "description": "AI revolutionizes medical science through data analysis and clinical decision-making.",
            "source": "https://example.com/ai-medical"
        }
    ]
}
````'''
    }
    
    test_response_3_backticks = {
        "output": '''```json
{
    "topics": [
        {
            "topic": "Machine Learning Applications",
            "description": "ML applications span various domains including healthcare and finance.",
            "source": "https://example.com/ml-apps"
        }
    ]
}
```'''
    }
    
    test_response_no_backticks = {
        "output": '''{
    "topics": [
        {
            "topic": "Data Science Trends",
            "description": "Current trends in data science include automated ML and explainable AI.",
            "source": "https://example.com/ds-trends"
        }
    ]
}'''
    }
    
    test_response_mixed = {
        "output": '''Here are the research findings:

````json
{
    "topics": [
        {
            "topic": "Natural Language Processing",
            "description": "NLP enables computers to understand and generate human language.",
            "source": "https://example.com/nlp"
        }
    ]
}
````

This completes the research.'''
    }
    
    test_cases = [
        ("4 backticks", test_response_4_backticks),
        ("3 backticks", test_response_3_backticks),
        ("No backticks", test_response_no_backticks),
        ("Mixed content", test_response_mixed)
    ]
    
    print("🧪 Testing Enhanced JSON Parsing")
    print("=" * 40)
    
    all_passed = True
    
    for test_name, test_response in test_cases:
        print(f"\n📝 Testing: {test_name}")
        try:
            result = parse_agent_response(test_response)
            if result and hasattr(result, 'topics') and len(result.topics) > 0:
                print(f"   ✅ Successfully parsed {len(result.topics)} topic(s)")
                print(f"   📄 Topic: {result.topics[0].topic}")
            else:
                print(f"   ❌ Failed to parse - empty result")
                all_passed = False
        except Exception as e:
            print(f"   ❌ Failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All JSON parsing tests passed!")
        print("🎉 The enhanced parser can handle various backtick formats")
    else:
        print("❌ Some tests failed")
    
    return all_passed

if __name__ == "__main__":
    test_json_parsing()
