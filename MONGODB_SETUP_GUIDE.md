# 🚀 LegalEase AI - MongoDB Setup Guide

## 📊 **MongoDB Migration Complete!**

Your LegalEase AI system has been successfully migrated from SQLite to MongoDB. Here's everything you need to know:

## 🔧 **MongoDB Installation & Setup**

### **1. Install MongoDB Community Server**

#### **Windows:**
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the setup wizard
3. Install MongoDB Compass (GUI tool) for easy database management

#### **macOS:**
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

#### **Linux (Ubuntu/Debian):**
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### **2. Start MongoDB Service**

#### **Windows:**
- MongoDB should start automatically after installation
- Or use: `net start MongoDB`

#### **macOS/Linux:**
```bash
# Start MongoDB
sudo systemctl start mongod
# Or on macOS: brew services start mongodb/brew/mongodb-community
```

### **3. Verify MongoDB is Running**
```bash
# Check MongoDB status
mongosh --eval "db.runCommand('ping')"
```

## 🗄️ **Database Configuration**

### **Environment Variables**
Create `backend/.env` file:
```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=legalease_ai

# AI APIs
GEMINI_API_KEY=your_gemini_api_key_here

# Application
DEBUG=true
```

### **MongoDB Collections Created**
The system will automatically create these collections:

1. **`contracts`** - Contract documents
2. **`contract_analyses`** - Analysis results
3. **`contract_clauses`** - Extracted clauses
4. **`clauses`** - Dataset clauses
5. **`users`** - User accounts
6. **`analysis_sessions`** - Analysis sessions

## 🚀 **Installation Steps**

### **1. Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **2. Start MongoDB**
Make sure MongoDB is running on `localhost:27017`

### **3. Start the Backend**
```bash
python main.py
```

## 📊 **MongoDB Compass Setup**

### **1. Download MongoDB Compass**
- Download from [mongodb.com/products/compass](https://www.mongodb.com/products/compass)
- Install and launch the application

### **2. Connect to Database**
- **Connection String:** `mongodb://localhost:27017`
- **Database Name:** `legalease_ai`

### **3. Explore Collections**
Once connected, you'll see:
- **contracts** - Uploaded contract files
- **contract_analyses** - AI analysis results
- **contract_clauses** - Extracted clauses with risk scores
- **clauses** - Dataset clauses for training

## 🔍 **Key MongoDB Features**

### **Document Structure**
```json
{
  "_id": "ObjectId",
  "contract_id": "string",
  "clause_text": "string",
  "clause_type": "confidentiality",
  "risk_level": "high",
  "risk_score": 8.5,
  "simplified_explanation": "string",
  "recommendations": ["array"],
  "created_at": "datetime"
}
```

### **Indexes Created**
- **Text Search:** Full-text search on clause text
- **Performance:** Indexes on contract_id, clause_type, risk_level
- **Sorting:** Indexes on analysis_date, risk_score

## 🎯 **MongoDB vs SQLite Benefits**

| Feature | SQLite | MongoDB |
|---------|--------|---------|
| **Scalability** | Single file | Distributed |
| **Performance** | Good for small apps | Excellent for large datasets |
| **Flexibility** | Fixed schema | Dynamic schema |
| **Search** | Basic SQL | Advanced text search |
| **Analytics** | Limited | Rich aggregation pipeline |
| **Cloud Support** | Manual backup | Built-in cloud features |

## 🔧 **Advanced MongoDB Features**

### **Text Search**
```javascript
// Search clauses by text
db.contract_clauses.find({
  $text: { $search: "confidentiality agreement" }
})
```

### **Aggregation Pipeline**
```javascript
// Get risk statistics
db.contract_clauses.aggregate([
  { $group: { 
    _id: "$risk_level", 
    count: { $sum: 1 },
    avg_score: { $avg: "$risk_score" }
  }}
])
```

### **Geospatial Queries** (Future)
```javascript
// Find contracts by location (if location data added)
db.contracts.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [lng, lat] },
      $maxDistance: 1000
    }
  }
})
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **MongoDB not starting:**
   ```bash
   # Check if MongoDB is running
   sudo systemctl status mongod
   
   # Start MongoDB
   sudo systemctl start mongod
   ```

2. **Connection refused:**
   - Ensure MongoDB is running on port 27017
   - Check firewall settings
   - Verify connection string in `.env`

3. **Permission denied:**
   ```bash
   # Fix MongoDB data directory permissions
   sudo chown -R mongodb:mongodb /var/lib/mongodb
   sudo chown -R mongodb:mongodb /var/log/mongodb
   ```

### **Performance Optimization**

1. **Create Indexes:**
   ```javascript
   // Create compound index
   db.contract_clauses.createIndex({
     "contract_id": 1,
     "risk_level": 1,
     "clause_type": 1
   })
   ```

2. **Monitor Performance:**
   ```javascript
   // Check slow queries
   db.setProfilingLevel(2, { slowms: 100 })
   db.system.profile.find().sort({ ts: -1 }).limit(5)
   ```

## 🎉 **Ready to Use!**

Your LegalEase AI system is now powered by MongoDB with:

- ✅ **MongoDB Integration** - NoSQL database for scalability
- ✅ **MongoDB Compass** - Visual database management
- ✅ **Advanced Search** - Full-text search capabilities
- ✅ **Flexible Schema** - Easy to add new fields
- ✅ **Cloud Ready** - Easy migration to MongoDB Atlas
- ✅ **Performance** - Optimized for large datasets

## 🔗 **Next Steps**

1. **Start MongoDB** service
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Set up environment:** Copy `.env.example` to `.env`
4. **Add Gemini API key** to `.env`
5. **Start the backend:** `python main.py`
6. **Open MongoDB Compass** to explore your data

Your LegalEase AI system is now ready for production-scale contract analysis! 🚀
