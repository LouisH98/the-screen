/*
An API that mirrors the REST API in the Python server
*/
import { ScreenStatus } from "./interfaces";

export async function getStatus(): Promise<ScreenStatus> {
    try {
        return fetch('http://unicorn.local:8000/status').then(res => res.json());
    } catch(e) {
        console.log("Error!", e);
        throw e;
    }
}