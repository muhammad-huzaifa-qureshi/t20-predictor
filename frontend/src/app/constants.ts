/**
 * Realistic match parameter ranges for T20 prediction models.
 */
export const MODEL_RANGES = {
  win: {
    target: { min: 40, max: 400, step: 1, hint: 'First innings total + 1 to win (40 - 400)' },
    score: { min: 0, max: 350, step: 1, hint: 'Innings runs scored so far (0 - 350)' },
    wickets: { min: 0, max: 9, step: 1, hint: 'Chasing wickets lost (0 - 9)' },
    balls_bowled: { min: 0, max: 119, step: 1, hint: 'Balls bowled in 2nd innings (0 - 119)' },
  },
  batting: {
    balls: { min: 1, max: 100, step: 1, hint: 'Balls the batter faced (1 - 100)' },
    fours: { min: 0, max: 25, step: 1, hint: 'Number of fours scored (0 - 25)' },
    sixes: { min: 0, max: 25, step: 1, hint: 'Number of sixes scored (0 - 25)' },
    strike_rate: { min: 0, max: 500, step: 0.01, hint: 'Runs / balls * 100 (0.00 - 500.00)' },
  },
  bowling: {
    fours: { min: 0, max: 16, step: 1, hint: 'Fours hit off this bowler (0 - 16)' },
    sixes: { min: 0, max: 12, step: 1, hint: 'Sixes hit off this bowler (0 - 12)' },
    balls: { min: 1, max: 24, step: 1, hint: 'Up to 24 legal balls (4 overs)' },
    economy: { min: 0, max: 36, step: 0.01, hint: 'Runs conceded per over (0.00 - 36.00)' },
  },
} as const;
