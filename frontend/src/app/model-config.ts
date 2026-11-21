import { MODEL_RANGES } from './constants';

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
        kind: 'win',
        title: 'Chase Win Probability',
        target: 'Win Probability',
        intro:
            'Calculate second-innings chase win probability using the target score and current match state.',
        example: { target: 180, score: 95, wickets: 2, balls_bowled: 66 },
        fields: [
            { key: 'target', label: 'Target score', hint: MODEL_RANGES.win.target.hint, min: MODEL_RANGES.win.target.min, max: MODEL_RANGES.win.target.max, step: MODEL_RANGES.win.target.step },
            { key: 'score', label: 'Current score', hint: MODEL_RANGES.win.score.hint, min: MODEL_RANGES.win.score.min, max: MODEL_RANGES.win.score.max, step: MODEL_RANGES.win.score.step },
            { key: 'wickets', label: 'Wickets lost', hint: MODEL_RANGES.win.wickets.hint, min: MODEL_RANGES.win.wickets.min, max: MODEL_RANGES.win.wickets.max, step: MODEL_RANGES.win.wickets.step },
            { key: 'balls_bowled', label: 'Balls bowled', hint: MODEL_RANGES.win.balls_bowled.hint, min: MODEL_RANGES.win.balls_bowled.min, max: MODEL_RANGES.win.balls_bowled.max, step: MODEL_RANGES.win.balls_bowled.step },
        ],
    },
    {
        kind: 'batting',
        title: 'Batting Performance',
        target: 'Batting Runs',
        intro:
            'Predict total innings runs based on balls faced, boundaries hit, and batting strike rate.',
        example: { balls: 20, fours: 3, sixes: 2, strike_rate: 150 },
        fields: [
            { key: 'balls', label: 'Balls faced', hint: MODEL_RANGES.batting.balls.hint, min: MODEL_RANGES.batting.balls.min, max: MODEL_RANGES.batting.balls.max, step: MODEL_RANGES.batting.balls.step },
            { key: 'fours', label: 'Fours hit', hint: MODEL_RANGES.batting.fours.hint, min: MODEL_RANGES.batting.fours.min, max: MODEL_RANGES.batting.fours.max, step: MODEL_RANGES.batting.fours.step },
            { key: 'sixes', label: 'Sixes hit', hint: MODEL_RANGES.batting.sixes.hint, min: MODEL_RANGES.batting.sixes.min, max: MODEL_RANGES.batting.sixes.max, step: MODEL_RANGES.batting.sixes.step },
            { key: 'strike_rate', label: 'Strike rate', hint: MODEL_RANGES.batting.strike_rate.hint, min: MODEL_RANGES.batting.strike_rate.min, max: MODEL_RANGES.batting.strike_rate.max, step: MODEL_RANGES.batting.strike_rate.step },
        ],
    },
    {
        kind: 'bowling',
        title: 'Bowling Spell',
        target: 'Runs Conceded',
        intro:
            'Predict total runs conceded based on spell length, boundaries conceded, and bowler economy.',
        example: { fours: 3, sixes: 1, balls: 24, economy: 8 },
        fields: [
            { key: 'fours', label: 'Fours conceded', hint: MODEL_RANGES.bowling.fours.hint, min: MODEL_RANGES.bowling.fours.min, max: MODEL_RANGES.bowling.fours.max, step: MODEL_RANGES.bowling.fours.step },
            { key: 'sixes', label: 'Sixes conceded', hint: MODEL_RANGES.bowling.sixes.hint, min: MODEL_RANGES.bowling.sixes.min, max: MODEL_RANGES.bowling.sixes.max, step: MODEL_RANGES.bowling.sixes.step },
            { key: 'balls', label: 'Balls bowled', hint: MODEL_RANGES.bowling.balls.hint, min: MODEL_RANGES.bowling.balls.min, max: MODEL_RANGES.bowling.balls.max, step: MODEL_RANGES.bowling.balls.step },
            { key: 'economy', label: 'Economy rate', hint: MODEL_RANGES.bowling.economy.hint, min: MODEL_RANGES.bowling.economy.min, max: MODEL_RANGES.bowling.economy.max, step: MODEL_RANGES.bowling.economy.step },
        ],
    },
];