#include "tabuleiro.h"

void Inicia_Tabuleiro(Tabuleiro* tab, int q){
    int i,j;
    if(q==1){
        for(i=0;i<M8;i++)
            for(j=0;j<M8;j++)
                tab->matriz8[i][j] = '0';
    }
    else if(q==2){
        for(i=0;i<M10;i++)
            for(j=0;j<M10;j++)
                tab->matriz10[i][j] = '0';
    }
     else if(q==3){
        for(i=0;i<M16;i++)
            for(j=0;j<M16;j++)
                tab->matriz16[i][j] = '0';
    }
    Coloca_Bomba(tab,q);
    Completa_Tabuleiro(tab,q);
}

void Print_Tabuleiro(Tabuleiro* tab, int q){
    int i,j;
    if(q==1){
        for(i=1;i<M8-1;i++){
            for(j=1;j<M8-1;j++)
                printf("%c ",tab->matriz8[i][j]);
            printf("\n");
        }
    }
    else if(q==2){
        for(i=1;i<M10-1;i++){
            for(j=1;j<M10-1;j++)
                printf("%c ",tab->matriz10[i][j]);
            printf("\n");
        }
    }
    else if(q==3){
        for(i=1;i<M16-1;i++){
            for(j=1;j<M16-1;j++)
                printf("%c ",tab->matriz16[i][j]);
            printf("\n");
        }
    }
    printf("\n\n");
}

void Coloca_Bomba(Tabuleiro* tab, int q){
    int bombas = 0;
    int posicao1, posicao2;
    if(q==1){
        srand( (unsigned)time(NULL) );
        while(bombas!=A){
            posicao1 = rand()%M8-1;
            posicao2 = rand()%M8-1;
            if(Posicao_Valida(q,posicao1, posicao2,0) && !Existe_Bomba(tab, posicao1, posicao2, q)){
                tab->matriz8[posicao1][posicao2] = '!';
                bombas++;
            }
        }
    }
    else if(q==2){
        srand( (unsigned)time(NULL) );
        while(bombas!=B){
            posicao1 = rand()%M10-1;
            posicao2 = rand()%M10-1;
            if(Posicao_Valida(q,posicao1, posicao2,0) && !Existe_Bomba(tab, posicao1, posicao2, q)){
                tab->matriz10[posicao1][posicao2] = '!';
                bombas++;
            }
        }
    }
    else if(q==3){
        srand( (unsigned)time(NULL) );
        while(bombas!=C){
            posicao1 = rand()%M16-1;
            posicao2 = rand()%M16-1;
            if(Posicao_Valida(q,posicao1, posicao2,0) && !Existe_Bomba(tab, posicao1, posicao2, q)){
                tab->matriz16[posicao1][posicao2] = '!';
                bombas++;
            }
        }
    }
}
void Coloca_Espaco(Tabuleiro* tab, int q){
    int linha,coluna;
    if(q==1){
        for(linha=1;linha<M8-1;linha++)
            for(coluna=1;coluna<M8-1;coluna++)
                if(tab->matriz8[linha][coluna]=='0')
                    tab->matriz8[linha][coluna] = '_';
    }
    else if(q==2){
        for(linha=1;linha<M10-1;linha++)
            for(coluna=1;coluna<M10-1;coluna++)
                if(tab->matriz10[linha][coluna]=='0')
                    tab->matriz10[linha][coluna] = '_';
    }
    else if(q==3){
        for(linha=1;linha<M16-1;linha++)
            for(coluna=1;coluna<M16-1;coluna++)
                if(tab->matriz16[linha][coluna]=='0')
                    tab->matriz16[linha][coluna] = '_';
    }
}

void Completa_Tabuleiro(Tabuleiro* tab, int q){
    int linha,coluna;
    if(q==1){
        for(linha=1;linha<M8-1;linha++){
            for(coluna=1;coluna<M8-1;coluna++){
                if(!Existe_Bomba(tab, linha, coluna, q)){
                    if(Existe_Bomba(tab, linha - 1, coluna - 1, q)) 
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha - 1, coluna, q)) 
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha - 1, coluna + 1, q))
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha, coluna - 1, q)) 
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha, coluna + 1, q)) 
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna - 1, q)) 
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna, q))
                        tab->matriz8[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna + 1, q))
                        tab->matriz8[linha][coluna]++;
                }
            }
        }
    }
    else if(q==2){
        for(linha=1;linha<M10-1;linha++){
            for(coluna=1;coluna<M10-1;coluna++){
                if(!Existe_Bomba(tab, linha, coluna, q)){
                    if(Existe_Bomba(tab, linha - 1, coluna - 1, q)) 
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha - 1, coluna, q)) 
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha - 1, coluna + 1, q))
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha, coluna - 1, q)) 
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha, coluna + 1, q)) 
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna - 1, q)) 
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna, q))
                        tab->matriz10[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna + 1, q))
                        tab->matriz10[linha][coluna]++;
                }
            }
        }
    }
    else if(q==3){
        for(linha=1;linha<M16-1;linha++){
            for(coluna=1;coluna<M16-1;coluna++){
                if(!Existe_Bomba(tab, linha, coluna, q)){
                    if(Existe_Bomba(tab, linha - 1, coluna - 1, q)) 
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha - 1, coluna, q)) 
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha - 1, coluna + 1, q))
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha, coluna - 1, q)) 
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha, coluna + 1, q)) 
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna - 1, q)) 
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna, q))
                        tab->matriz16[linha][coluna]++;
                    if(Existe_Bomba(tab, linha + 1, coluna + 1, q))
                        tab->matriz16[linha][coluna]++;
                }
            }
        }
    }
    Coloca_Espaco(tab, q);
}


int Existe_Bomba(Tabuleiro* tab, int i, int j,int q){
    if(q==1){
        if(tab->matriz8[i][j] == '!') return 1;
        return 0; 
    }
    else if(q==2){
        if(tab->matriz10[i][j] == '!') return 1;
        return 0; 
    }
    else if(q==3){
       if(tab->matriz16[i][j] == '!') return 1;
        return 0;  
    }
}

int Existe_Espaco(Tabuleiro* tab, int i, int j,int q){
    if(q==1){
        if(tab->matriz8[i][j] == '_') return 1;
        return 0; 
    }
    else if(q==2){
        if(tab->matriz10[i][j] == '_') return 1;
        return 0; 
    }
    else if(q==3){
       if(tab->matriz16[i][j] == '_') return 1;
        return 0;  
    }
}

int Existe_Numero(Tabuleiro* tab, int i, int j,int q){
    if(!Existe_Espaco(tab, i, j, q) && !Existe_Bomba(tab, i, j, q)) return 1;
    return 0; 
}

int Posicao_Valida(int q, int posicao1, int posicao2, int i){
     if(q==1){
       if(posicao1 > 0 && posicao1 < M8-1 && posicao2 > 0 && posicao2 < M8-1) return 1;
    }
    else if(q==2){
        if(posicao1 > 0 && posicao1 < M10-1 && posicao2 > 0 && posicao2 < M10-1) return 1;
    }
    else if(q==3){
        if(posicao1 > 0 && posicao1 < M16-1 && posicao2 > 0 && posicao2 < M16-1) return 1;
    }
    if(i){
        printf("\n\033[4;31m POSICAO INVALIDA!!!!\n");
        printf("Digite uma posicao valida \033[m\n");
    }
    return 0;
}
