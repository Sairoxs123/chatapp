# Quick Start & Testing Guide

## Installation

1. **Install Dependencies**
```bash
pip install django channels django-cors-headers
```

2. **Run the Server**
```bash
cd /home/runner/work/chatapp/chatapp
python manage.py runserver
```

3. **Access the Application**
```
http://127.0.0.1:8000/
```

## Testing Checklist

### ✅ 1. WebSocket Connection Test
**What to check**: WebSocket establishes connection properly

**Steps**:
1. Log in to the application
2. Navigate to a chat (direct or group)
3. Open browser console (F12)
4. Look for: `WebSocket connected` message

**Expected**: Console shows successful WebSocket connection
**Issue if**: Shows connection errors or "Reconnecting..." continuously

---

### ✅ 2. Real-Time Messaging Test
**What to check**: Messages appear instantly in real-time

**Steps**:
1. Open two different browsers (or incognito + normal)
2. Log in with different users in each browser
3. Open chat between the two users
4. Send a message from Browser 1
5. Watch Browser 2

**Expected**: Message appears instantly in Browser 2 without refresh
**Issue if**: Message doesn't appear or requires page refresh

---

### ✅ 3. Search Functionality Test
**What to check**: Search works without page reload

**Steps**:
1. Go to dashboard/home page
2. Type a username in the search box
3. Observe the user list

**Expected**: 
- User list filters instantly as you type
- Clearing search restores full list
- No page reload/flicker

**Issue if**: Page reloads or search doesn't filter

---

### ✅ 4. Image Upload Test
**What to check**: Images can be uploaded and appear in chat

**Steps**:
1. Open a chat
2. Click the image/photo button
3. Select an image file
4. Click "Send Image"
5. Wait for upload

**Expected**: 
- Image appears in chat
- Modal closes automatically
- Image is clickable to view full size

**Issue if**: Upload fails or image doesn't appear

---

### ✅ 5. Message Deletion Test
**What to check**: Own messages can be deleted

**Steps**:
1. Send a message
2. Hover over your own message
3. Click the × (delete) button
4. Watch in second browser (if available)

**Expected**: 
- Message disappears from both browsers
- Deletion happens in real-time

**Issue if**: Message doesn't delete or requires refresh

---

### ✅ 6. Group Chat Test
**What to check**: Group chats work with multiple users

**Steps**:
1. Create a group with multiple members
2. Open group chat
3. Send messages
4. Check member list displays correctly

**Expected**:
- All members see messages in real-time
- Member avatars/names show correctly
- Admin badge shows for group admins

**Issue if**: Messages don't sync or members not shown

---

### ✅ 7. Reconnection Test
**What to check**: WebSocket reconnects after network interruption

**Steps**:
1. Open a chat
2. Open browser DevTools (F12) → Network tab
3. Find the WebSocket connection (ws://...)
4. Right-click and "Close connection"
5. Wait a few seconds

**Expected**: 
- Status shows "Reconnecting..."
- Connection re-establishes automatically
- Messages still work after reconnection

**Issue if**: Stays disconnected or requires page refresh

---

### ✅ 8. Mobile Responsiveness Test
**What to check**: UI works on mobile screen sizes

**Steps**:
1. Open DevTools (F12)
2. Click mobile device toggle (Ctrl+Shift+M)
3. Try different screen sizes
4. Test all features

**Expected**:
- Layout adjusts properly
- All buttons/inputs are accessible
- Text is readable
- No horizontal scroll

**Issue if**: Layout breaks or elements overlap

---

### ✅ 9. Multiple Concurrent Chats Test
**What to check**: Multiple chat windows work simultaneously

**Steps**:
1. Open multiple browser tabs
2. Open different chats in each tab
3. Send messages in different tabs
4. Verify all update correctly

**Expected**: Each chat maintains its own WebSocket and updates independently

**Issue if**: Chats interfere with each other

---

### ✅ 10. Browser Console Error Check
**What to check**: No JavaScript errors during normal use

**Steps**:
1. Open browser console (F12)
2. Use all features (send message, search, upload, delete)
3. Watch for red error messages

**Expected**: No errors in console during normal use
**Issue if**: Red error messages appear

---

## Common Issues & Solutions

### WebSocket Connection Failed
**Symptom**: Console shows WebSocket errors
**Solution**: 
- Ensure Django Channels is installed: `pip install channels`
- Check ASGI_APPLICATION in settings.py
- Verify server is running with ASGI support

### Messages Not Appearing
**Symptom**: Messages don't show in real-time
**Solution**:
- Check WebSocket connection in console
- Verify both users are in same room
- Check server logs for errors

### Image Upload Fails
**Symptom**: Images don't upload or show errors
**Solution**:
- Check MEDIA_ROOT and MEDIA_URL in settings
- Verify media folder has write permissions
- Check browser console for CSRF errors

### Search Doesn't Work
**Symptom**: Search doesn't filter users
**Solution**:
- Check browser console for errors
- Verify `/main/search` endpoint returns JSON
- Clear browser cache

### Slow Performance
**Symptom**: App feels sluggish
**Solution**:
- Check if old polling code is still running (should not be)
- Verify incremental message loading is working
- Check network tab for excessive requests

---

## Performance Monitoring

### What to Monitor
1. **Network Tab**: Should see 1 WebSocket connection, minimal HTTP requests
2. **Console**: Should show "WebSocket connected", no repeated polling
3. **Memory**: Should not increase continuously (no memory leaks)
4. **CPU**: Should be low during idle time

### Expected Behavior
- **Page Load**: ~2-5 HTTP requests total
- **Messaging**: 0 additional HTTP requests (WebSocket only)
- **Latency**: Messages appear in <50ms
- **Bandwidth**: ~10-20KB/minute during active chat

---

## Success Criteria

✅ WebSocket connection established on chat pages
✅ Messages appear in real-time (<50ms)
✅ Search works without page reload
✅ Images upload successfully
✅ No polling visible in Network tab
✅ Mobile responsive on all screen sizes
✅ No console errors during normal use
✅ Auto-reconnection works after disconnection

If all above pass, the improvements are working correctly! 🎉

---

## Need Help?

Check the documentation:
- `SUMMARY.md` - Quick overview
- `IMPROVEMENTS.md` - Technical details
- `COMPARISON.md` - Before/after comparison

Look for console messages:
- "WebSocket connected" = ✅ Good
- "WebSocket error" = ❌ Check installation
- No WebSocket messages = ❌ Check ASGI config
