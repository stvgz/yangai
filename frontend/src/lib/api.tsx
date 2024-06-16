// src/lib/api.js
import axios from 'axios';
import {text} from "node:stream/consumers";

// const API_BASE_URL = process.env.API_BASE_URL || 'https://production-url.com';
const API_BASE_URL ='http://127.0.0.1:8000';

export const getConversations = async() => {
    const response = await axios.get(`${API_BASE_URL}/conversations`);
    return response.data;
};
// export const createProduct = (data) => axios.post(`${API_BASE_URL}/products`, data);


export const getConversationByID = async(id: string) => {
    const response = await axios.get(`${API_BASE_URL}/conversation-by-id/${id}`);
    return response.data;
}


export const getConversationByIDwithSentence = async(id: string) => {
    const response = await axios.get(`${API_BASE_URL}/conversation-by-id-with-sentences/${id}`);
    return response.data;
}

export const updateLabelSentence = async(sentence_id: number, label_text: string, label_score: number ) => {
    const response: any = await axios.post(`${API_BASE_URL}/label-sentence/`, {
        sentence_id,
        label_text,
        label_score
    });
    return response.data;
}