import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { ModelKind } from './model-config';

export interface Contribution {
    label: string;
    input: number;
    value: number;
}

export interface PredictionResponse {
    model: ModelKind;
    target: string;
    prediction: number;
    unit: string;
    base: number;
    contributions: Contribution[];
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
    private readonly http = inject(HttpClient);
    predict(kind: ModelKind, payload: Record<string, number>):
        Observable<PredictionResponse> {
        return this.http.post<PredictionResponse>(`/api/predict/${kind}`,
            payload);
    }
}