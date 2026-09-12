# AI Course Generation System
This project contains a short AI-generated course on structured outputs, designed for a learner whose pipeline breaks when model responses include prose instead of JSON.
The generator builds lessons and coding exercises step-by-step while carrying prior lesson content and learner code across generation stages.

## Course Goal
The capstone is a schema-validated structured output pipeline with a repair loop.

## Checkpoints

Lesson 1:
- Learner can now instruct the model to return an output in a fixed shape (prompt instruction + JSON mode)
- Learner can now extract the JSON from a response using a regular expression

Lesson 2:
- Learner can validate the response against a schema
- Learner can now diagnose a failed response and retry, using a loop that feeds the response and its schema error back into the model
- Learner can now stop the pipeline and flag the failure, using an exception

## Project Structure
- `agent/`: generation prompts, orchestration, validation logic, and extraction
- `build/`: learner based build alongs and the Python artifacts they produce
- `course/`: AI-generated lesson sections
- `output/`: terminal outputs from running learner artifacts
- `writeup.md`: submission reflection

## Running the Builds
Python 3.12 is required.
Run all commands from the project root directory.

To install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

To run Lesson 1 build:
```bash
python3 build/lesson-1/pipeline.py
```

To run Lesson 2 build:
```bash
python3 build/lesson-2/pipeline.py
```

Build 2 extends the exact `pipeline.py` produced in Build 1, rather than starting over.
Actual outputs from running the builds are saved in `output/lesson-1.txt` and `output/lesson-2.txt`.

## Course Generation
The course sections and build alongs were generated using NVIDIA Nemotron 3 Super through OpenRouter.
The `agent/` folder contains the prompts, course structure, generation orchestration, extraction, and validation logic.
Course generation requires an `OPENROUTER_API_KEY` in a `.env` file.

To generate the course:
```bash
python3 agent/run_agent.py
```

To generate the build alongs:
```bash
python3 agent/run_build_agent.py
```

Generation requires an API key, but the generated learner builds do not. The builds use cached model responses, so they can be reviewed offline.