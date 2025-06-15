# Run Flask App
1. Run python app.py
2. Go to 127.0.0.1:5000
3. Click on 'Generate video'
4. Enter your story in maximum 3 sentences
5. Click on Generate video.

# Run RAG script
1. Run python .\scripts\rag_example.py
2. Input any questions on the generated screenplays
3. See the response
4. Ask any number of questions on the screenplays one after the other
5. Input 'quit' to exit.

# Run MCP scripts
1. Python .\scripts\mcp_server_example.py
2. Python .\scripts\mcp_client_example.py

# Running the main application application
python main.py -k <TOGETHER_APIKEY>
               -o <OPEN_AI_APIKEY>
               -l <LEONARDO_AI_APIKEY>
               -s <STORY_NUMBER>