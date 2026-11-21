export type ModelKind = 'batting' | 'bowling' | 'win';

export interface FieldSpec {
    key: string;
    label: string;
    hint?: string;
    min: number;
    max: number;
    step: number;
}

export interface ModelSpec {
    kind: ModelKind;
    title: string;
    target: string;
    intro?: string;
    example?: Record<string, number>;
    fields: FieldSpec[];
}

export const MODELS: ModelSpec[] = [
    {
        kind: 'batting',
        title: 'Batting',
        target: 'Runs',
        intro:
            'Enter the stats of a completed innings. The model returns the runs that usually go with them.',
        example: { balls: 20, fours: 3, sixes: 2, strike_rate: 150 },
        fields: [
            { key: 'balls', label: 'Balls faced', hint: 'Balls the batter faced', min: 1, max: 120, step: 1 },
            { key: 'fours', label: 'Fours', hint: 'Number of fours hit', min: 0, max: 60, step: 1 },
            { key: 'sixes', label: 'Sixes', hint: 'Number of sixes hit', min: 0, max: 60, step: 1 },
            { key: 'strike_rate', label: 'Strike rate', hint: 'Runs ÷ balls × 100', min: 0, max: 720, step: 0.01 },
        ],
    },
    {
        kind: 'bowling',
        title: 'Bowling',
        target: 'Runs conceded',
        intro:
            'Enter the figures of a completed spell. The model returns the runs conceded that usually go with them.',
        example: { fours: 3, sixes: 1, balls: 24, economy: 8 },
        fields: [
            { key: 'fours', label: 'Fours conceded', hint: 'Fours hit off the bowler', min: 0, max: 24, step: 1 },
            { key: 'sixes', label: 'Sixes conceded', hint: 'Sixes hit off the bowler', min: 0, max: 24, step: 1 },
            { key: 'balls', label: 'Balls bowled', hint: 'Up to 24 balls (4 overs)', min: 1, max: 24, step: 1 },
            { key: 'economy', label: 'Economy rate', hint: 'Runs conceded per over', min: 0, max: 60, step: 0.01 },
        ],
    },
    {
        kind: 'win',
        title: 'Win Probability',
        target: 'Win Probability',
        intro: 'Enter the match situation during a chase. The model calculates the batting team\'s win probability.',
        example: { target: 180, score: 95, wickets: 2, balls_bowled: 66 },
        fields: [
            { key: 'target', label: 'Target score', hint: 'Runs needed to win + 1', min: 1, max: 350, step: 1 },
            { key: 'score', label: 'Current score', hint: 'Runs scored so far in the chase', min: 0, max: 349, step: 1 },
            { key: 'wickets', label: 'Wickets lost', hint: 'Wickets lost by chasing team (0-9)', min: 0, max: 9, step: 1 },
            { key: 'balls_bowled', label: 'Balls bowled (Max. 120)', hint: 'Balls bowled so far in the chase', min: 0, max: 119, step: 1 },
        ],
    },
];