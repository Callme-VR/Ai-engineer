import json

# Read the notebook
with open('Rnnimplenmentation.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find and fix the cell with the error (cell index 3, execution_count 44)
for cell in notebook['cells']:
    if cell['cell_type'] == 'code' and 'X_last=Rnn(X)' in ''.join(cell['source']):
        # Fix the error: change X_last=Rnn(X) to X_last=Rnn(x)
        for i, line in enumerate(cell['source']):
            if 'X_last=Rnn(X)' in line:
                cell['source'][i] = line.replace(
                    'X_last=Rnn(X)', 'X_last=Rnn(x)')
                print(
                    f"✅ Fixed line: {line.strip()} -> {cell['source'][i].strip()}")

        # Clear the error output since we're fixing it
        cell['outputs'] = []
        cell['execution_count'] = None
        break

# Save the corrected notebook
with open('Rnnimplenmentation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n🎉 Notebook fixed successfully!")
print("The error 'X_last=Rnn(X)' has been corrected to 'X_last=Rnn(x)'")
print("Please reload the notebook in Jupyter to see the changes.")
