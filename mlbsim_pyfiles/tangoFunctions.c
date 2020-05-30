#include<stdio.h>
#include<math.h>
#define MAXRUNS 25

void getInningProb(float[], float, int);
float get9InnProb(float inningProb[], int n);
void getGameProb(float inningProb[], float gameProb[], float RG, int hFA);
void getSim(float[], float[], float(*)[MAXRUNS]);

int main()
{
    /*
    // initialize arrays to hold inning, game, and sim probability distributions
    float inningProb_team1[MAXRUNS];
    float inningProb_team2[MAXRUNS];
    float gameProb_team1[MAXRUNS] = {0};
    float gameProb_team2[MAXRUNS] = {0};
    float simProb[MAXRUNS][MAXRUNS];

    // initialize variables to hold user inputs
    float team1_RG;
    float team2_RG;
    
    // user input for each teams R/G
    printf("Home team R/G -> ");
    scanf("%f", &team1_RG);
    //printf("Away team R/G -> ");
    //scanf("%f", &team2_RG);
    
    // function calls to get run distribution
    getGameProb(inningProb_team1, gameProb_team1, team1_RG, 0);
    //getGameProb(inningProb_team2, gameProb_team2, team2_RG, 0);

    int i;
    for(i = 0; i < MAXRUNS; i++)
        printf("prob[%d] = %.4f\n", i, 100 * gameProb_team1[i]);
        
    //getSim(gameProb_team1, gameProb_team2, simProb);    

    return(0);
    */
    
}

void getInningProb(float inningProb[], float runsPerGame, int hFA)
{
    // Change R/G to R/I
    float runsPerInn = runsPerGame / 9;

    // Define constants
    int i; // counter for 2+ runs for loop
    float c = 0.767;
    float a = c * pow(runsPerInn, 2);

    // add home team advantage
    if(hFA == 1)
        runsPerInn += 0.075 / 9;
    else if(hFA == -1)
        runsPerInn -= 0.075 / 9;

    // Calculate probability of n runs
    inningProb[0] = runsPerInn / (runsPerInn + a);
    float d = 1 - c * inningProb[0];
    inningProb[1] =  (1 - inningProb[0]) * (1 - d);
    for(i = 2; i < MAXRUNS; i++)
        inningProb[i] = inningProb[i-1] * d;
}

float get9InnProb(float inningProb[], int n)
{
    int i1, i2, i3, i4, i5, i6, i7, i8, i9;
    float prob = 0;

    for(i1 = n; i1 >= 0; i1--)
        for(i2 = n-i1; i2 >= 0; i2--)
            for(i3 = n-i1-i2; i3 >= 0; i3--)
                for(i4 = n-i1-i2-i3; i4 >= 0; i4--)
                    for(i5 = n-i1-i2-i3-i4; i5 >= 0; i5--)
                        for(i6 = n-i1-i2-i3-i4-i5; i6 >= 0; i6--)
                            for(i7 =n-i1-i2-i3-i4-i5-i6; i7 >= 0; i7--)
                                for(i8 = n-i1-i2-i3-i4-i5-i6-i7; i8 >= 0; i8--)
                                    for(i9 = n-i1-i2-i3-i4-i5-i6-i7-i8; i9 >= 0; i9--)
                                        if(i1+i2+i3+i4+i5+i6+i7+i8+i9 == n)
                                            prob += inningProb[i1]*inningProb[i2]*inningProb[i3]*inningProb[i4]*inningProb[i5]*inningProb[i6]*inningProb[i7]*inningProb[i8]*inningProb[i9];
    return(prob);

}

void getGameProb(float inningProb[], float gameProb[], float RG, int hFA)
{
    getInningProb(inningProb, RG, hFA);
    int n;
    for(n = 0; n < MAXRUNS; n++)
        gameProb[n] = get9InnProb(inningProb, n);
}

void getSim(float gameProb1[], float gameProb2[], float (*simProb)[MAXRUNS])
{
    int i, j;
    float winProb_team1 = 0;
    float winProb_team2 = 0;
    float ties = 0;
    float sum = 0;

    // create probability matrix of every possible combination
    for(i = 0; i < MAXRUNS; i++)
    {
        for(j = 0; j < MAXRUNS; j++)
        {
            simProb[i][j] = gameProb1[i] * gameProb2[j];
            sum += simProb[i][j];
        }
    }

    for(i = 0; i < MAXRUNS; i++)
    {
        for(j = 0; j < MAXRUNS; j++)
        {
            if(i > j)
                winProb_team1 += simProb[i][j];
            else if(j > i)
                winProb_team2 += simProb[i][j];
            else if(i == j)
                ties += simProb[i][j];
        }
    }

    /*
    printf("Total prob = %.2f\n", winProb_team1 + winProb_team2);

    winProb_team1 += 0.53 * ties;
    winProb_team2 += 0.47 * ties;
    
    printf("\nHome team win %% = %.2f %%\n", winProb_team1 * 100);
    printf("Away team win %% = %.2f %%\n", winProb_team2 * 100);
    printf("Tie probability =  %.2f %%\n", (1 - winProb_team1 - winProb_team2) * 100);
    */
   
}
