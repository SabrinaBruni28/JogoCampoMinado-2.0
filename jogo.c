#include "jogo.h"

void Inicia_Jogo(Jogo* jog, int q){
    int i,j;
    if(q==1){
        for(i=0;i<M8;i++)
            for(j=0;j<M8;j++)
                jog->matriz8[i][j] = '0';
    }
    else if(q==2){
        for(i=0;i<M10;i++)
            for(j=0;j<M10;j++)
                jog->matriz10[i][j] = '0';
    }
     else if(q==3){
        for(i=0;i<M16;i++)
            for(j=0;j<M16;j++)
                jog->matriz16[i][j] = '0';
    }
}

void Print_Jogo(Jogo* jog, int q){
    int i,j;
    printf("\n\n");
    if(q==1){
        for(i=1;i<M8-1;i++){
            printf("\t");
            for(j=1;j<M8-1;j++){
                if(jog->matriz8[i][j] == '0')
                    printf("\033[1m%c \033[m",jog->matriz8[i][j]);
                else if(jog->matriz8[i][j] == '_')
                    printf("\033[1;37m%c \033[m",jog->matriz8[i][j]);
                else if(jog->matriz8[i][j] == '!')
                    printf("\033[1;31m%c \033[m",jog->matriz8[i][j]);
                else if(jog->matriz8[i][j] == 'X')
                    printf("\033[1;33m%c \033[m",jog->matriz8[i][j]);
                else if(jog->matriz8[i][j] == '^')
                    printf("\033[1;36m%c \033[m",jog->matriz8[i][j]);
                else if(jog->matriz8[i][j] == '?')
                    printf("\033[1;35m%c \033[m",jog->matriz8[i][j]);
                else
                    printf("\033[1;32m%c \033[m",jog->matriz8[i][j]);
            }
            printf("\n");
        }
    }
    else if(q==2){
        for(i=1;i<M10-1;i++){
            printf("\t");
            for(j=1;j<M10-1;j++){
                if(jog->matriz10[i][j] == '0')
                    printf("\033[1m%c \033[m",jog->matriz10[i][j]);
                else if(jog->matriz10[i][j] == '_')
                    printf("\033[1;37m%c \033[m",jog->matriz10[i][j]);
                else if(jog->matriz10[i][j] == '!')
                    printf("\033[1;31m%c \033[m",jog->matriz10[i][j]);
                else if(jog->matriz10[i][j] == 'X')
                    printf("\033[1;33m%c \033[m",jog->matriz10[i][j]);
                else if(jog->matriz10[i][j] == '^')
                    printf("\033[1;36m%c \033[m",jog->matriz10[i][j]);
                 else if(jog->matriz10[i][j] == '?')
                    printf("\033[1;35m%c \033[m",jog->matriz10[i][j]);
                else
                    printf("\033[1;32m%c \033[m",jog->matriz10[i][j]);
            }
            printf("\n");
        }
    }
    else if(q==3){
        for(i=1;i<M16-1;i++){
            printf("\t");
            for(j=1;j<M16-1;j++){
                if(jog->matriz16[i][j] == '0')
                    printf("\033[1m%c \033[m",jog->matriz16[i][j]);
                else if(jog->matriz16[i][j] == '_')
                    printf("\033[1;37m%c \033[m",jog->matriz16[i][j]);
                else if(jog->matriz16[i][j] == '!')
                    printf("\033[1;31m%c \033[m",jog->matriz16[i][j]);
                else if(jog->matriz16[i][j] == 'X')
                    printf("\033[1;33m%c \033[m",jog->matriz16[i][j]);
                else if(jog->matriz16[i][j] == '^')
                    printf("\033[1;36m%c \033[m",jog->matriz16[i][j]);
                 else if(jog->matriz16[i][j] == '?')
                    printf("\033[1;35m%c \033[m",jog->matriz16[i][j]);
                else
                    printf("\033[1;32m%c \033[m",jog->matriz16[i][j]);
            }
            printf("\n");
        }
    }
    printf("\n\n");
}

int Revela_Quadrado(Jogo* jog, Tabuleiro* tab, int q, int posicao1, int posicao2, int *aberto, int *bandeira){
    int i,j;
    if(Posicao_Valida(q, posicao1, posicao2,1) && Ja_Foi_Aberto(jog, q, posicao1, posicao2, 1)){
        if(Existe_Bomba(tab, posicao1, posicao2, q)){
            Fim_De_Jogo(jog, tab, q);
            Explodiu(jog, q, posicao1, posicao2);
            return 1;
        }
        else if(Existe_Espaco(tab, posicao1, posicao2, q))
            Abrir_Espaco(jog, tab, q, posicao1, posicao2, aberto);
        else if(Existe_Numero(tab, posicao1, posicao2, q)){
            Abrir_Posicao(jog, tab, q, posicao1, posicao2);
            *aberto += 1;
        }
    }
    if(Ganhou_Jogo(jog, q,  posicao1, posicao2, *aberto, *bandeira)) return 1;
    return 0;
}

int Existe_Alerta(Jogo * jog, int i, int j,int q){
    if(q==1){
        if(jog->matriz8[i][j] == '?') return 1;
        return 0; 
    }
    else if(q==2){
        if(jog->matriz10[i][j] == '?') return 1;
        return 0; 
    }
    else if(q==3){
       if(jog->matriz16[i][j] == '?') return 1;
        return 0;  
    }
}


void Fim_De_Jogo(Jogo* jog, Tabuleiro* tab, int q){
    int i,j, tam;

    if(q==1) tam = M8-1;
    else if(q==2) tam = M10-1;
    else if(q==3) tam = M16-1;

    for(i=1;i<tam;i++){
        for(j=1;j<tam;j++){
            if(Existe_Bomba(tab, i, j, q) && !Existe_Alerta(jog, i, j, q))
                Abrir_Posicao(jog, tab, q, i, j);
            else Errado(jog, tab, q, i, j);
        }
    }
    printf("\n\n\033[4;31m ******** FIM DE JOGO!!! ********\n");
    printf("******** VOCE PERDEU!! ******** \033[m\n");
}

void Abrir_Espaco(Jogo* jog, Tabuleiro* tab, int q, int posicao1, int posicao2, int* aberto){
    if (Posicao_Valida(q, posicao1, posicao2,0) && Ja_Foi_Aberto(jog, q, posicao1, posicao2, 0)) {
        if(Existe_Espaco(tab, posicao1, posicao2, q) || Existe_Numero(tab, posicao1, posicao2, q)){
            Abrir_Posicao(jog, tab, q, posicao1, posicao2);
            *aberto += 1;
        }
        if(Existe_Espaco(tab, posicao1, posicao2, q)){
            Abrir_Espaco(jog, tab, q, posicao1 - 1, posicao2 - 1, aberto);
            Abrir_Espaco(jog, tab, q, posicao1 - 1, posicao2, aberto);
            Abrir_Espaco(jog, tab, q, posicao1 - 1, posicao2 + 1, aberto);
            Abrir_Espaco(jog, tab, q, posicao1, posicao2 - 1, aberto);
            Abrir_Espaco(jog, tab, q, posicao1, posicao2 + 1, aberto);
            Abrir_Espaco(jog, tab, q, posicao1 + 1, posicao2 - 1, aberto);
            Abrir_Espaco(jog, tab, q, posicao1 + 1, posicao2,aberto);
            Abrir_Espaco(jog, tab, q, posicao1 + 1, posicao2 + 1,aberto);
        }
    }
}

int Ja_Foi_Aberto(Jogo* jog, int q, int posicao1, int posicao2, int i){
    if(q==1){
       if(jog->matriz8[posicao1][posicao2] == '0') return 1;
    }
    else if(q==2){
        if(jog->matriz10[posicao1][posicao2] == '0') return 1;
    }
    else if(q==3){
        if(jog->matriz16[posicao1][posicao2] == '0') return 1;
    }
    if(i){
        printf("\n\033[4;31m POSICAO JA ABERTA OU COM BANDEIRA!!!!\n");
        printf("Digite uma posicao que esteja fechada \033[m\n");
    }
    return 0;
}

void Abrir_Posicao(Jogo* jog, Tabuleiro* tab, int q, int posicao1, int posicao2){
    if(q==1)
        jog->matriz8[posicao1][posicao2] = tab->matriz8[posicao1][posicao2]; 
    else if(q==2)
        jog->matriz10[posicao1][posicao2] = tab->matriz10[posicao1][posicao2]; 
    else if(q==3)
        jog->matriz16[posicao1][posicao2] = tab->matriz16[posicao1][posicao2];
}

int Ganhou_Jogo(Jogo* jog, int q, int i, int j, int aberto, int bandeira){
    if(q==1){
        if(aberto == (M8-2)*(M8-2)-(A) && bandeira == A){
            printf("\n\n\033[4;32m ******** PARABENS!!! ********\n");
            printf("******* VOCE GANHOU!!!!!! ******** \033[m\n");
            return 1;
        }
    }
    else if(q==2){
        if(aberto == (M10-2)*(M10-2)-(B) && bandeira == B){
            printf("\n\n\033[4;32m ******** PARABENS!!! ********\n");
            printf("******* VOCE GANHOU!!!!!! ******** \033[m\n");
            return 1;
        }
    }
    else if(q==3){
        if(aberto == (M16-2)*(M16-2)-(C) && bandeira == C){
            printf("\n\n\033[4;32m ******** PARABENS!!! ********\n");
            printf("******* VOCE GANHOU!!!!!! ******** \033[m\n");
            return 1;
        }
    }
    return 0;
}

void Colocar_Alerta(Jogo* jog, int q, int posicao1, int posicao2, int *bandeira){
    if(Posicao_Valida(q, posicao1, posicao2,1) && Ja_Foi_Aberto(jog, q, posicao1, posicao2,1) && !Existe_Alerta(jog, posicao1, posicao2, q)){
        if(q==1)
            jog->matriz8[posicao1][posicao2] = '?';
        else if(q==2)
            jog->matriz10[posicao1][posicao2] = '?';
        else if(q==3)
            jog->matriz16[posicao1][posicao2] = '?';
        *bandeira += 1;
    }
}
int Tira_Alerta(Jogo* jog, int q, int posicao1, int posicao2, int *bandeira){
    if(Posicao_Valida(q, posicao1, posicao2,1) && Existe_Alerta(jog, posicao1, posicao2, q)){
        if(q==1)
            jog->matriz8[posicao1][posicao2] = '0';
        else if(q==2)
            jog->matriz10[posicao1][posicao2] = '0';
        else if(q==3)
            jog->matriz16[posicao1][posicao2] = '0';
        *bandeira -= 1;
        return 1;
    }
    printf("\n\033[4;31m POSICAO NAO CONTEM UM ALERTA!!! \033[m\n");
    return 0;
}

void Errado(Jogo* jog,Tabuleiro* tab, int q, int posicao1, int posicao2){
    if(Existe_Alerta(jog, posicao1, posicao2, q) && !Existe_Bomba(tab, posicao1, posicao2, q)){
        if(q==1)
            jog->matriz8[posicao1][posicao2] = '^'; 
        else if(q==2)
            jog->matriz10[posicao1][posicao2] = '^'; 
        else if(q==3)
            jog->matriz16[posicao1][posicao2] = '^';
    }
}

void Explodiu(Jogo* jog, int q, int posicao1, int posicao2){
    if(q==1)
        jog->matriz8[posicao1][posicao2] = 'X'; 
    else if(q==2)
       jog->matriz10[posicao1][posicao2] = 'X'; 
    else if(q==3)
        jog->matriz16[posicao1][posicao2] = 'X';
}
