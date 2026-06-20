import os
import sys
from google import genai
from google.genai import types

# -------------------------------------------------------------
# SECURE CLIENT INITIALIZATION
# -------------------------------------------------------------
# Fetching the API key from environment variables for production security
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("[CRITICAL ERROR]: 'GEMINI_API_KEY' environment variable is missing!", file=sys.stderr)
    print("Please run the container with: -e GEMINI_API_KEY='your_key'", file=sys.stderr)
    sys.exit(1)

# Initializing the SDK Client using the new Google GenAI library standard
client = genai.Client(api_key=GEMINI_API_KEY)


# -------------------------------------------------------------
# AGENT 1: The Generator (Dockerfile Creator)
# -------------------------------------------------------------
def generate_dockerfile(tech_stack, feedback_logs=None):
    """
    Generates a high-performance Dockerfile based on the tech stack.
    If feedback logs exist, it optimizes the previous code to fix compliance or build errors.
    """
    # Enhanced prompt instructions to guarantee compliance with python versions >= 3.10
    sys_instruction = (
        "You are an expert Enterprise DevOps Engineer. Your task is to write a highly optimized Dockerfile "
        "for the given technology stack.\n"
        "PRODUCTION MANDATES:\n"
        "1. Base images MUST use Python 3.11-slim or higher. Do NOT use python:3.9 or lower as dependencies require Python >= 3.10.\n"
        "2. Multi-stage build is STRICTLY REQUIRED. Use a build stage (AS builder) for dependencies and a final minimal stage for execution.\n"
        "3. Clean up cache after package installation to keep the layer and image size small.\n"
        "CRITICAL RULE: Return ONLY the raw Dockerfile code. "
        "Do NOT use markdown code blocks (like ```dockerfile) or any conversational text."
    )
    
    if not feedback_logs:
        user_prompt = (
            f"Generate a compliant multi-stage Dockerfile for a {tech_stack}. "
            f"The directory contains an 'app.py' file as the main entry point."
        )
    else:
        user_prompt = (
            f"The previous Dockerfile was REJECTED during validation or build.\n"
            f"Tech Stack: {tech_stack}\n"
            f"Feedback / Error Logs:\n{feedback_logs}\n"
            f"Please analyze the errors carefully and generate a corrected, compliance-ready multi-stage Dockerfile."
        )

    print("[Generator Agent]: Writing/Optimizing multi-stage Dockerfile configuration...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(system_instruction=sys_instruction)
    )
    return response.text.strip()


# -------------------------------------------------------------
# AGENT 2: The Pre-Build Validator (Compliance Guardrails)
# -------------------------------------------------------------
def validate_dockerfile(dockerfile_content):
    """
    Performs static analysis on the generated Dockerfile string against corporate standards.
    Acts as a 'Shift-Left' security layer before executing real hardware build commands.
    """
    print("[Validator Agent]: Scanning Dockerfile against enterprise production best practices...")
    
    sys_instruction = (
        "You are a corporate Chief Security Officer (CSO). Validate the provided Dockerfile "
        "strictly against the following enterprise compliance rules:\n\n"
        "RULES TO CHECK:\n"
        "1. IMMUTABILITY: Base images must NOT use the ':latest' tag. A fixed version tag is mandatory.\n"
        "2. SECURITY: The container must not run as 'root'. A non-root 'USER' directive must be explicitly defined.\n"
        "3. OPTIMIZATION: Multi-stage build architecture MUST be used (look for multiple 'FROM' statements).\n\n"
        "OUTPUT FORMAT:\n"
        "- If all 3 rules pass, reply with exactly one word: APPROVED\n"
        "- If any rule is violated, reply with: REJECTED - [Provide explicit details on what needs to be fixed]"
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Validate this Dockerfile configuration:\n\n{dockerfile_content}",
        config=types.GenerateContentConfig(system_instruction=sys_instruction)
    )
    return response.text.strip()


# -------------------------------------------------------------
# THE ORCHESTRATOR: Evaluator-Optimizer Engine Loop
# -------------------------------------------------------------
def main_loop():
    tech_stack = "Python application with app.py"
    max_attempts = 4
    current_attempt = 1
    feedback = None  
    
    while current_attempt <= max_attempts:
        print(f"\n--- PIPELINE ATTEMPT {current_attempt} OF {max_attempts} ---")
        
        # Step 1: Automated Multi-Stage Generation
        dockerfile_code = generate_dockerfile(tech_stack, feedback)
        
        # Step 2: Pre-Build Governance Check
        validation_result = validate_dockerfile(dockerfile_code)
        print(f"[Validator Verdict]: {validation_result}")
        
        # Step 3: Evaluation Routing
        if "REJECTED" in validation_result:
            print("Compliance check failed! Routing context back to the Generator Agent.")
            feedback = validation_result  
            current_attempt += 1
            continue  
            
        # Step 4: Workspace Deployment (Only if APPROVED)
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_code)
        print("Compliant Dockerfile successfully staged and saved to workspace.")
        print("PIPELINE STATUS: PASSED COMPLIANCE! Ready for continuous integration build pipelines.")
        break
        
    if current_attempt > max_attempts:
        print("\nPIPELINE STATUS: FAILED! Maximum optimization cycles reached. Manual intervention required.")

if __name__ == "__main__":
    main_loop()
