# 🔧 Fix Pylance Errors - Quick Guide

## ❌ Common Errors You're Seeing

### 1. "Import 'pydantic' could not be resolved"
### 2. "'List' is not accessed"
### 3. "Import is not accessed"

---

## ✅ **QUICK FIX (2 Minutes)**

### Option 1: Run Setup Script (EASIEST)

```bash
cd /home/victormayowa/geron-mamasafe
./setup-python.sh
```

Then restart your editor!

---

### Option 2: Manual Setup

#### Step 1: Create Virtual Environment
```bash
cd /home/victormayowa/geron-mamasafe/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 2: Select Interpreter

**In VS Code/Windsurf:**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P`)
2. Type: `Python: Select Interpreter`
3. Select: `./backend/venv/bin/python`

#### Step 3: Reload Window
1. Press `Ctrl+Shift+P`
2. Type: `Developer: Reload Window`
3. Press Enter

---

## ✅ **What I've Already Fixed**

I created configuration files for you:

### 1. `.vscode/settings.json`
- Automatically points Pylance to your virtual environment
- Configures Python path correctly

### 2. `pyrightconfig.json`
- Configures Pylance/pyright settings
- Reduces false-positive warnings

### 3. `setup-python.sh`
- One-command setup script
- Installs all dependencies

---

## 🎯 **Understanding the Errors**

### Error 1: "Import could not be resolved"
**Cause:** Python environment not selected or packages not installed

**Fix:**
```bash
# Install packages
cd backend
pip install -r requirements.txt

# Select interpreter in editor
# Ctrl+Shift+P > Python: Select Interpreter
```

### Error 2: "'List' is not accessed"
**Cause:** Importing `List` from `typing` but not using it

**Fix:** Either:
- Remove unused imports
- OR ignore the warning (it's just informational)

### Error 3: "Import is not accessed"
**Cause:** Same as above - imported but not used

**Fix:** Remove unused imports or ignore

---

## 🔥 **NUCLEAR OPTION (If Nothing Works)**

### Disable Pylance Type Checking

Create `.vscode/settings.json`:
```json
{
    "python.analysis.typeCheckingMode": "off",
    "python.analysis.diagnosticMode": "off"
}
```

**Note:** This disables type checking but your code will still work fine!

---

## ✅ **Verify It's Working**

After setup, you should see:
- ✅ No red underlines under imports
- ✅ Pylance shows "Python 3.x.x ('venv': venv)" in status bar
- ✅ Autocomplete works for pydantic, FastAPI, etc.

---

## 🆘 **Still Having Issues?**

### Check if packages are installed:
```bash
cd backend
source venv/bin/activate
pip list | grep pydantic
pip list | grep fastapi
```

### Check which Python is selected:
```bash
which python
# Should show: /home/victormayowa/geron-mamasafe/backend/venv/bin/python
```

### Reinstall if needed:
```bash
pip install --force-reinstall -r requirements.txt
```

---

## 💡 **Pro Tips**

### For Windsurf Users:
- Same as VS Code (uses same underlying system)
- `Ctrl+Shift+P` > `Python: Select Interpreter`

### For Cursor Users:
- Same commands work
- Might need to reload window after selecting interpreter

### For PyCharm Users:
- File > Settings > Project > Python Interpreter
- Add interpreter > Select `./backend/venv/bin/python`

---

## 🎉 **Expected Result**

After fixing, all these should work:
- ✅ No Pylance errors
- ✅ Autocomplete for FastAPI, Pydantic, etc.
- ✅ Go to definition works
- ✅ Type hints show correctly

---

**Run the setup script and reload your editor!** 💚

```bash
./setup-python.sh
```
