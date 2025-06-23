from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT ="""
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'True' or 'False') Does that actual response match the expected response?
"""

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

def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response = expected_response,
        actual_response = response_text,
    )
    
    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()
    
    print(prompt)
    
    if "True" in evaluation_results_str_cleaned:
        # print response in green if it is correct
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "False" in evaluation_results_str_cleaned:
        # Print response in red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'True' or 'False'."
        )
        