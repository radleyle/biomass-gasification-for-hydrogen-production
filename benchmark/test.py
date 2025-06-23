from query_data import query_rag
from langchain_community.llms.ollama import Ollama
import pytest

EVAL_PROMPT ="""
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does that actual response match the expected response?
"""

# === BASIC HAPPY PATH TESTS ===
def test_hydrogen_yield_peak_temperature():
    assert query_and_validate(
        question="What is the hydrogen yield at peak gasification temperature of 500°C? (Answer with the number and unit only)",
        expected_response="4.7 mol/kg",
    )

def test_co2_yield_peak_temperature():
    assert query_and_validate(
        question="What is the CO2 yield at peak gasification temperature of 500°C? (Answer with the number and unit only)",
        expected_response="3.6 mol/kg",
    )

def test_hydrogen_yield_90_minutes():
    assert query_and_validate(
        question="What is the hydrogen yield at 90 minutes reaction time? (Answer with the number and unit only)",
        expected_response="2.4 mol/kg",
    )

def test_reactor_capacity():
    assert query_and_validate(
        question="What is the capacity of the SWGR batch reactor used in the study? (Answer with the number and unit only)",
        expected_response="300 ml",
    )

def test_peak_hydrogen_efficiency():
    assert query_and_validate(
        question="What is the peak hydrogen efficiency (HE) achieved in the study? (Answer with the number and unit only)",
        expected_response="9.2%",
    )

def test_peak_cold_gas_efficiency():
    assert query_and_validate(
        question="What is the peak cold gas efficiency (CGE) achieved in the study? (Answer with the number and unit only)",
        expected_response="6.7%",
    )

def test_waste_heat_recovery_rate():
    assert query_and_validate(
        question="What is the peak waste heat recovery rate mentioned in the study? (Answer with the number and unit only)",
        expected_response="23.1%",
    )

def test_methane_yield_peak_temperature():
    assert query_and_validate(
        question="What is the CH4 yield at peak gasification temperature of 500°C? (Answer with the number and unit only)",
        expected_response="2.6 mol/kg",
    )

def test_gasification_temperatures():
    assert query_and_validate(
        question="What are the three gasification temperatures tested in the study? (Answer with numbers and units, separated by commas)",
        expected_response="400°C, 450°C, 500°C",
    )

def test_reaction_times():
    assert query_and_validate(
        question="What are the three reaction times tested in the study? (Answer with numbers and units, separated by commas)",
        expected_response="30 min, 60 min, 90 min",
    )

# === EDGE CASE TESTS: BOUNDARY VALUES ===
def test_hydrogen_yield_at_400_celsius():
    assert query_and_validate(
        question="What is the hydrogen yield at 400°C gasification temperature? (Answer with the number and unit only)",
        expected_response="Should find value from data",  # You'll need to replace with actual expected value
    )

def test_hydrogen_yield_at_30_minutes():
    assert query_and_validate(
        question="What is the hydrogen yield at 30 minutes reaction time? (Answer with the number and unit only)",
        expected_response="Should find value from data",  # You'll need to replace with actual expected value
    )

# === EDGE CASE TESTS: ALTERNATIVE PHRASING ===
def test_reactor_capacity_alternative_phrasing():
    assert query_and_validate(
        question="What is the volume of the SWGR reactor? (Answer with the number and unit only)",
        expected_response="300 ml",
    )

def test_hydrogen_yield_alternative_units():
    """Test if system can handle equivalent unit expressions"""
    assert query_and_validate_flexible(
        question="What is the hydrogen yield at peak gasification temperature of 500°C? (Answer with the number and unit only)",
        acceptable_responses=["4.7 mol/kg", "4.70 mol/kg", "4.7 mol kg⁻¹"],
    )

# === EDGE CASE TESTS: MISSING DATA ===
def test_nonexistent_temperature():
    """Test behavior when asking for data that doesn't exist"""
    response = query_rag("What is the hydrogen yield at 600°C gasification temperature?")
    # Should indicate data not available rather than hallucinating
    assert any(phrase in response.lower() for phrase in [
        "not found", "not available", "no data", "not mentioned", "not specified"
    ]), f"Expected indication of missing data, got: {response}"

def test_nonexistent_time():
    """Test behavior when asking for data that doesn't exist"""
    response = query_rag("What is the hydrogen yield at 120 minutes reaction time?")
    assert any(phrase in response.lower() for phrase in [
        "not found", "not available", "no data", "not mentioned", "not specified"
    ]), f"Expected indication of missing data, got: {response}"

# === EDGE CASE TESTS: MALFORMED QUESTIONS ===
def test_empty_question():
    """Test behavior with empty question"""
    response = query_rag("")
    # Should handle gracefully, not crash
    assert response is not None and len(response) > 0, "Empty question should return some response"

def test_very_long_question():
    """Test behavior with extremely long question"""
    long_question = "What is the hydrogen yield " + "at peak gasification temperature " * 20 + "of 500°C?"
    response = query_rag(long_question)
    assert response is not None, "Long question should not cause system failure"

def test_ambiguous_question():
    """Test behavior with ambiguous question"""
    response = query_rag("What is the yield?")  # No specification of which yield
    assert response is not None, "Ambiguous question should return some response"

# === EDGE CASE TESTS: COMPARATIVE QUESTIONS ===
def test_temperature_comparison():
    """Test comparative analysis"""
    assert query_and_validate_contains(
        question="Which temperature gives the highest hydrogen yield: 400°C, 450°C, or 500°C?",
        expected_content="500°C",
    )

def test_time_comparison():
    """Test comparative analysis for reaction times"""
    assert query_and_validate_contains(
        question="At which reaction time is hydrogen yield highest: 30, 60, or 90 minutes?",
        expected_content="90",  # Assuming longer time gives higher yield
    )

# === HELPER FUNCTIONS ===

def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response = expected_response,
        actual_response = response_text,
    )
    
    model = Ollama(model="mistral")
    
    try:
        evaluation_results_str = model.invoke(prompt)
        evaluation_results_str_cleaned = evaluation_results_str.strip().lower()
        
        print(f"\n{'='*80}")
        print(f"QUESTION: {question}")
        print(f"ACTUAL RESPONSE: {response_text}")
        print(f"EXPECTED: {expected_response}")
        print(f"{'='*80}")
        print(prompt)
        print(f"{'='*80}")
        
        if "true" in evaluation_results_str_cleaned:
            print("\033[92m" + f"✅ PASS: {evaluation_results_str_cleaned}" + "\033[0m")
            return True
        elif "false" in evaluation_results_str_cleaned:
            print("\033[91m" + f"❌ FAIL: {evaluation_results_str_cleaned}" + "\033[0m")
            return False
        else:
            print("\033[93m" + f"⚠️  UNCLEAR EVALUATION: {evaluation_results_str_cleaned}" + "\033[0m")
            raise ValueError(
                f"Invalid evaluation result. Cannot determine if 'True' or 'False'. Got: {evaluation_results_str_cleaned}"
            )
    except Exception as e:
        print(f"\033[91m❌ ERROR during evaluation: {str(e)}\033[0m")
        raise

def query_and_validate_flexible(question: str, acceptable_responses: list):
    """Test with multiple acceptable responses"""
    response_text = query_rag(question)
    
    for expected_response in acceptable_responses:
        prompt = EVAL_PROMPT.format(
            expected_response=expected_response,
            actual_response=response_text,
        )
        
        model = Ollama(model="mistral")
        evaluation_results_str = model.invoke(prompt)
        
        if "true" in evaluation_results_str.strip().lower():
            print(f"\n{'='*80}")
            print(f"QUESTION: {question}")
            print(f"ACTUAL RESPONSE: {response_text}")
            print(f"MATCHED EXPECTED: {expected_response}")
            print("\033[92m" + f"✅ PASS: Response matches one acceptable format" + "\033[0m")
            return True
    
    print(f"\n{'='*80}")
    print(f"QUESTION: {question}")
    print(f"ACTUAL RESPONSE: {response_text}")
    print(f"ACCEPTABLE RESPONSES: {acceptable_responses}")
    print("\033[91m" + f"❌ FAIL: Response doesn't match any acceptable format" + "\033[0m")
    return False

def query_and_validate_contains(question: str, expected_content: str):
    """Test if response contains expected content (less strict)"""
    response_text = query_rag(question)
    
    print(f"\n{'='*80}")
    print(f"QUESTION: {question}")
    print(f"ACTUAL RESPONSE: {response_text}")
    print(f"LOOKING FOR: {expected_content}")
    print(f"{'='*80}")
    
    if expected_content.lower() in response_text.lower():
        print("\033[92m" + f"✅ PASS: Response contains expected content" + "\033[0m")
        return True
    else:
        print("\033[91m" + f"❌ FAIL: Response doesn't contain expected content" + "\033[0m")
        return False
        