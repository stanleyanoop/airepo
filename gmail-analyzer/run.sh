!#/bin/sh

echo "START : Processing and deleting the gmails"
echo "Starting the venv"
python3 -m venv lc-agent-env
source lc-agent-env/bin/activate
echo "Starting the script"
python app.py >> run.log
echo "Script execution completed. Deactivating the venv"
deactivate
echo "END : Processing and deleting the gmails"
