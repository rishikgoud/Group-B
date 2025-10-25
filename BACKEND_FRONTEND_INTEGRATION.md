# Backend-Frontend Integration Guide

## 🎯 Overview

The LegalEase AI frontend is now fully integrated with the FastAPI backend, providing a seamless user experience with real-time data, error handling, and loading states.

## 🔗 Integration Features

### ✅ **API Service Layer**
- **Location**: `frontend/src/services/api.ts`
- **Features**:
  - Axios-based HTTP client with interceptors
  - Automatic request/response logging
  - Centralized error handling
  - Type-safe API calls

### ✅ **Custom React Hooks**
- **Location**: `frontend/src/hooks/useAPI.ts`
- **Features**:
  - Loading states management
  - Error handling
  - Automatic data fetching
  - Manual API execution

### ✅ **Updated Components**
- **Dashboard**: Real contract upload and listing
- **Analytics**: Live dataset statistics and charts
- **Dataset Explorer**: New page for exploring clauses
- **Error Handling**: Comprehensive error states and retry functionality

## 🚀 Quick Start

### 1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

### 3. **Environment Configuration**
Copy environment files:
```bash
# Backend
cp backend/env.example backend/.env

# Frontend
cp frontend/env.example frontend/.env
```

## 📊 API Integration Details

### **Contract Management**
- **Upload**: `POST /api/v1/contracts/upload`
- **List**: `GET /api/v1/contracts/list`
- **Details**: `GET /api/v1/contracts/{id}`
- **Delete**: `DELETE /api/v1/contracts/{id}`

### **Analysis**
- **Analyze**: `POST /api/v1/analysis/analyze`
- **Risk Levels**: `GET /api/v1/analysis/risk-levels`
- **Clause Types**: `GET /api/v1/analysis/clause-types`

### **Dataset**
- **Clauses**: `GET /api/v1/dataset/clauses`
- **Stats**: `GET /api/v1/dataset/stats`
- **Types**: `GET /api/v1/dataset/clauses/types/list`
- **Risk Levels**: `GET /api/v1/dataset/clauses/risk-levels/list`

### **Health Check**
- **Basic**: `GET /health/`
- **Detailed**: `GET /health/detailed`

## 🎨 Frontend Features

### **Dashboard Page**
- ✅ **File Upload**: Drag & drop with progress indicators
- ✅ **Contract List**: Real-time data from backend
- ✅ **Status Indicators**: Processed/Pending states
- ✅ **Error Handling**: Retry functionality

### **Analytics Page**
- ✅ **Live Statistics**: Real dataset metrics
- ✅ **Interactive Charts**: Risk distribution and clause types
- ✅ **Loading States**: Smooth loading animations
- ✅ **Error Recovery**: Graceful error handling

### **Dataset Explorer** (New!)
- ✅ **Search & Filter**: Text search, clause type, risk level
- ✅ **Pagination**: Efficient data loading
- ✅ **Clause Details**: Full text and simplified explanations
- ✅ **Risk Indicators**: Color-coded risk levels

### **Navigation**
- ✅ **Updated Navbar**: Added Dataset Explorer link
- ✅ **Responsive Design**: Mobile-friendly navigation
- ✅ **Active States**: Visual feedback for current page

## 🔧 Technical Implementation

### **API Service Architecture**
```typescript
// Centralized API client
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/${API_VERSION}`,
  timeout: 30000,
});

// Request/Response interceptors
api.interceptors.request.use(/* logging */);
api.interceptors.response.use(/* error handling */);
```

### **Custom Hooks Pattern**
```typescript
// Generic API hook
export const useAPI = <T>(apiCall: () => Promise<{ data: T }>) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // ... implementation
};
```

### **Error Handling**
```typescript
// Centralized error handling
export const handleAPIError = (error: any) => {
  if (error.response) {
    return { message: error.response.data.detail, status: error.response.status };
  }
  // ... network and other errors
};
```

## 📱 User Experience Features

### **Loading States**
- **Spinners**: Consistent loading animations
- **Skeleton Screens**: Placeholder content during loading
- **Progress Indicators**: Upload progress feedback

### **Error Handling**
- **Toast Notifications**: User-friendly error messages
- **Retry Buttons**: Easy error recovery
- **Fallback UI**: Graceful degradation

### **Data Management**
- **Real-time Updates**: Automatic data refresh
- **Optimistic Updates**: Immediate UI feedback
- **Caching**: Efficient data management

## 🧪 Testing the Integration

### **1. Health Check**
```bash
curl http://localhost:8000/health/
```

### **2. Upload Test**
1. Go to http://localhost:3000/dashboard
2. Upload a sample PDF file
3. Verify it appears in the contracts list

### **3. Analytics Test**
1. Go to http://localhost:3000/analytics
2. Verify charts load with real data
3. Check statistics are accurate

### **4. Dataset Explorer Test**
1. Go to http://localhost:3000/dataset
2. Test search and filtering
3. Verify pagination works

## 🔍 Debugging

### **Frontend Console**
- **API Logs**: All requests/responses logged
- **Error Messages**: Detailed error information
- **Network Tab**: Monitor API calls

### **Backend Logs**
- **Startup**: Database and dataset loading
- **API Calls**: Request/response logging
- **Errors**: Detailed error traces

### **Common Issues**

1. **CORS Errors**:
   - Check backend CORS configuration
   - Verify frontend API URL

2. **Network Errors**:
   - Ensure backend is running on port 8000
   - Check firewall settings

3. **Data Loading Issues**:
   - Verify database initialization
   - Check dataset loading

## 🚀 Next Steps

### **Immediate Improvements**
1. **Authentication**: Add user login/logout
2. **File Processing**: Implement PDF text extraction
3. **Real Analysis**: Connect AI services
4. **Caching**: Add Redis for performance

### **Advanced Features**
1. **Real-time Updates**: WebSocket integration
2. **Offline Support**: Service worker implementation
3. **Advanced Search**: Full-text search capabilities
4. **Export Features**: PDF/Excel export functionality

## 📈 Performance Considerations

### **Frontend**
- **Code Splitting**: Lazy load components
- **Memoization**: Optimize re-renders
- **Bundle Size**: Monitor and optimize

### **Backend**
- **Database Indexing**: Optimize queries
- **Caching**: Implement response caching
- **Rate Limiting**: Prevent abuse

## 🎉 Integration Complete!

The backend and frontend are now fully integrated with:
- ✅ **Real-time data** from FastAPI backend
- ✅ **Comprehensive error handling** and loading states
- ✅ **Modern React patterns** with custom hooks
- ✅ **Responsive design** with Tailwind CSS
- ✅ **Type-safe API** communication
- ✅ **User-friendly** interface with toast notifications

The application is ready for development and testing!
