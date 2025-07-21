import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
    applicationId: process.env.REACT_APP_APPLICATION_ID,
    clientToken: process.env.REACT_APP_CLIENT_TOKEN,
    site: 'datadoghq.com',
    service: 'rum_headers_example',
    env: 'dev',
    // Specify a version number to identify the deployed version of your application in Datadog
    // version: '1.0.0', 
    sessionSampleRate: 100,
    sessionReplaySampleRate: 100,
    trackUserInteractions: true,
    trackResources: true,
    trackLongTasks: true,
    defaultPrivacyLevel: 'mask-user-input',

    // ----------------
    // Headers Testing
    // ----------------

    // All of the below configurations create a rum event associated with a trace and headers in
    // the outgoing http fetch request

    //allowedTracingUrls: ["https://dummyjson.com/"],
    //allowedTracingUrls: [ { match: "https://dummyjson.com/", propagatorTypes: ["datadog"] } ],
    /* => Generates X-Datadog headers:
      X-Datadog-Origin: rum
      X-Datadog-Parent-Id: 4848410277313398643
      X-Datadog-Sampling-Priority: 1
      X-Datadog-Trace-Id: 6527759828729824762
    */

    //allowedTracingUrls: [ { match: "https://dummyjson.com/", propagatorTypes: ["b3"] } ],
    /* => Generates B3 single header:
      B3: 00bac47fbfcfcc76-0f63bb1ccb315b87-1
    */

    //allowedTracingUrls: [ { match: "https://dummyjson.com/", propagatorTypes: ["b3multi"] } ],
    /* => Generates B3 headers:
      X-B3-Sampled: 1
      X-B3-Spanid: 586efd88b5980084
      X-B3-Traceid: 7ad88c5ea74958aa
    */

    // ----------------
    // Regex Testing
    // ----------------

    allowedTracingUrls: [ { match: /https:\/\/dummyjson\.com\//, propagatorTypes: ["b3"] } ],
    /* => Generates B3 single header:
      B3: 00bac47fbfcfcc76-0f63bb1ccb315b87-1
    */
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
