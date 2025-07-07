import React, { useEffect } from 'react';
import messaging from '@react-native-firebase/messaging';
import { View, Text, Button, Alert } from 'react-native';

const App = () => {
  useEffect(() => {
    const getToken = async () => {
      try {
        const token = await messaging().getToken();
        console.log('FCM Token:', token);

        // Send token to backend
        await fetch('http://13.126.236.52:5000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token }),
        });
      } catch (error) {
        console.error('Error getting or sending token:', error);
      }
    };

    getToken();

    const unsubscribe = messaging().onMessage(async remoteMessage => {
      Alert.alert('Notification', remoteMessage.notification?.title || 'No title');
    });

    return unsubscribe;
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Real-Time Notification App</Text>
    </View>
  );
};

export default App;
