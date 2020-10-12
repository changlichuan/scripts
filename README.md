# scripts
Written in Python3

- Create an .env file to avoid prompted with ACCESS_TOKEN each time
- Add LIMIT= entry in .env to overwrite paging limit with each request
- Add HISTORY= entry in .env to overwrite date range of chat histories to be pulled

execute by "python load_Threads.py"

Current version stores all outputs in memory, under variables members / threads / messages. Please implement own Data Access logic to save into harddisk. 


