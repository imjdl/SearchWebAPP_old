#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/if_packet.h>
#include <netinet/if_ether.h>
#include <netinet/in.h>
//#include <signal.h>

typedef struct _iphdr { //定义IP首部
    unsigned char h_verlen; //4位首部长度+4位IP版本号
    unsigned char tos; //8位服务类型TOS
    unsigned short total_len; //16位总长度（字节）
    unsigned short ident; //16位标识
    unsigned short frag_and_flags; //3位标志位
    unsigned char ttl; //8位生存时间 TTL
    unsigned char proto; //8位协议 (TCP, UDP 或其他)
    unsigned short checksum; //16位IP首部校验和
    unsigned int sourceIP; //32位源IP地址
    unsigned int destIP; //32位目的IP地址
}IP_HEADER;
typedef struct _tcphdr { //定义TCP首部
    unsigned short th_sport; //16位源端口
    unsigned short th_dport; //16位目的端口
    unsigned int th_seq; //32位序列号
    unsigned int th_ack; //32位确认号
    unsigned char th_lenres;//4位首部长度/6位保留字
    unsigned char th_flag; //6位标志位
    unsigned short th_win; //16位窗口大小
    unsigned short th_sum; //16位校验和
    unsigned short th_urp; //16位紧急数据偏移量
}TCP_HEADER;
typedef struct { // 定义返回的数据结构
    unsigned int src_port; //返回的源端口号
    unsigned int dst_port; //返回的目的端口号
    unsigned char* src_ip; //源地址
    unsigned char* dst_ip; //目的地址
} BACK_DATA;
int getdata(char *filename,int flag);
BACK_DATA * analyse(IP_HEADER *ip,TCP_HEADER *tcp);
int getdata_sock ;
static int isstop = 0;
/*
    注意:正式加载时应将main注释掉 防止多重定义
*/
void stop(){
    close(getdata_sock);
    isstop = 1;
}
int main(int argv, char *args[]){
//    signal(SIGINT,stoprecv);
    getdata("port.csv",1);
    return 0;
}
int getdata(char *filename,int flag){
	char buf[10240];
    unsigned int n;
    IP_HEADER *ip;
	getdata_sock = socket(PF_PACKET,  SOCK_DGRAM, htons(ETH_P_IP));
	if(getdata_sock<0){
		printf("socket Error");
		exit(-1);
    }
    while(1){
        if(isstop != 0){
            break;
        }
        n = recv(getdata_sock, buf, sizeof(buf), 0);
        if (n == -1)
        {
            printf("recv error!\n");
            break;
        }
        else if (n==0)
            continue;
        ip = ( IP_HEADER *)(buf);
        size_t iplen =  (ip->h_verlen&0x0f)*4;
        TCP_HEADER *tcp = (TCP_HEADER *)(buf +iplen);
        if (ip->proto == IPPROTO_TCP)
        {
            TCP_HEADER *tcp = (TCP_HEADER *)(buf +iplen);
            BACK_DATA* backdata = NULL;
            backdata = analyse(ip,tcp);
            if(backdata != NULL){
//                FILE *f = fopen(filename,"ab+");
                printf("hhh%u\n",backdata->src_port);
                if(flag == 0){
                     printf("%u.%u.%u.%u\n",backdata->src_ip[0],backdata->src_ip[1],
                                        backdata->src_ip[2],backdata->src_ip[3]);
                }else{
                    printf("%u\n",backdata->src_port);
                }
//                fclose(f);
            }
        }
    }
	return 0;
}

BACK_DATA * analyse(IP_HEADER *ip,TCP_HEADER *tcp){
    BACK_DATA *backdata = NULL;
    if(ntohs(tcp->th_dport) == 10010 & ntohs(tcp->th_flag) == 4608){
//        printf("Source port: %u\n", ntohs(tcp->th_sport));
//        printf("Dest port: %u\n", ntohs(tcp->th_dport));
//        printf("flag %u\n",ntohs(tcp->th_flag));
//        unsigned char* p = (unsigned char*)&ip->sourceIP;
//        printf("Source IP\t: %u.%u.%u.%u\n",p[0],p[1],p[2],p[3]);
//        p = (unsigned char*)&ip->destIP;
//        printf("Destination IP\t: %u.%u.%u.%u\n",p[0],p[1],p[2],p[3]);

        backdata = (BACK_DATA *)malloc(sizeof(BACK_DATA));
        backdata->src_port = ntohs(tcp->th_sport);
        backdata->dst_port = ntohs(tcp->th_dport);
        backdata->src_ip = (unsigned char*)&ip->sourceIP;
        backdata->dst_ip = (unsigned char*)&ip->destIP;
    }
    return backdata;
}
