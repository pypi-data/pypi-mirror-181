//ϵͳ
#ifdef WIN32
#include "pch.h"
#endif

#include "vnhft.h"
#include "pybind11/pybind11.h"
#include "hft/hft_trader_api.h"


using namespace pybind11;
using namespace HFT;



///-------------------------------------------------------------------------------------
///C++ SPI�Ļص���������ʵ��
///-------------------------------------------------------------------------------------

//API�ļ̳�ʵ��
class TdApi : public TraderSpi
{
private:
	TraderApi* api;            //API����
    bool active = false;       //����״̬

public:
    TdApi()
    {
    };

    ~TdApi()
    {
        if (this->active)
        {
            this->exit();
        }
    };

    //-------------------------------------------------------------------------------------
    //API�ص�����
    //-------------------------------------------------------------------------------------

    /**
     * ���ӶϿ�ʱ�ص�
     */
    virtual void OnDisconnect();

    /**
     * ������Ϣ�ص���ϵͳ����ʱ�Ż�ص�
     *
     * @param error_info    ������Ϣ
     * @param request_id    ��Ӧ����ʱ��������кţ�����������󴥷��Ĵ��󣬴��ֶ�ֵΪ0
     */
    virtual void OnError(ErrorInfo* error_info, int request_id = 0);

    /**
     * ��ظ澯��Ϣ֪ͨ�ص�
     *
     * @param risk_notify   ��ظ澯��Ϣ
     */
    virtual void OnRiskNotify(RiskNotify* risk_notify);

    /**
    * ����֪ͨ��Ϣ�ص�
    *
    * @param failback_notify   ����֪ͨ��Ϣ
    */
    virtual void OnFailBackNotify(FailBackNotify* failback_notify);

    /**
     * ��¼�ɹ���ʧ��ʱ�ص�
     *
     * @param rsp           ��¼Ӧ�����ݣ������ͻ��š��ͻ��������ɶ��������Ϣ
     * @param error_info    ������Ϣ
     */
    virtual void OnLogin(LoginRsp* rsp, ErrorInfo* error_info);

    /**
     * �ɽ��ر��ص�
     *
     * @param trade_detail  �ص��ĳɽ��������
     */
    virtual void OnTradeReport(TradeDetail* trade_detail);

    /**
     * ����״̬�仯�ص�
     *
     * @param order_detail  �ص��Ķ�������
     */
    virtual void OnOrderStatus(OrderDetail* order_detail);

    /**
     * ����ί�е���Ӧ
     * Order��BatchOrder��AppointContractSellStockRepay���ɴ˽ӿ���Ӧ
     *
     * @param order_rsp     ����ί��Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnOrderRsp(OrderRsp* order_rsp, ErrorInfo* error_info, int request_id,
        bool is_last);

    /**
     * ��������Ӧ
     *
     * @param cancel_rsp    ����Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnCancelRsp(CancelRsp* cancel_rsp, ErrorInfo* error_info, int request_id,
        bool is_last);

    /**
     * ��ѯ���ն����������Ӧ��һ�η���һ����������
     * QueryOrder��QueryOrderByCode��QueryOrders���ɴ˽ӿ���Ӧ
     *
     * @param order_detail  ��������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryOrderRsp(OrderDetail* order_detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ���ճɽ��������Ӧ��һ�η���һ���ɽ�����
     * QueryTradeByCode��QueryTradeByOrderId��QueryTrades��QueryETFTrades���ɴ˽ӿ���Ӧ
     *
     * @param trade_detail  �ɽ�����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryTradeRsp(TradeDetail* trade_detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ���ճֲ��������Ӧ��һ�η���һ���ֲ�����
     * QueryPosition��QueryPositions�ɴ˽ӿ���Ӧ
     *
     * @param position_detail   �ֲ�����
     * @param error_info        Ӧ��Ĵ�����Ϣ
     * @param request_id        ��Ӧ����ʱ��������к�
     * @param is_last           �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str           ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryPositionRsp(PositionDetail* position_detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ�����ʽ����Ӧ
     *
     * @param cash_detail   �ʽ�����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryCashRsp(CashDetail* cash_detail, ErrorInfo* error_info, int request_id);

    /**
     * �鼯�н���ϵͳ�����ʽ�
     *
     * @param avail_balance �����ʽ𣬵�λ�������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnQueryJZJYAvailFundRsp(int64_t avail_balance, ErrorInfo* error_info,
        int request_id);

    /**
     * ���н��׹�̨����ٹ�̨֮���ʽ�ת��ת��
     *
     * @param transfer_value    ��ת���
     * @param error_info        Ӧ��Ĵ�����Ϣ
     * @param request_id        �������кţ�����ƥ����Ӧ�����û��Զ���
     */
    virtual void OnTransferFundInAndOutRsp(int64_t transfer_value, ErrorInfo* error_info,
        int request_id);

    /**
     * ���ͬһ���ʽ��˺ţ�һ������֮���ʽ�ת
     *
     * @param transfer_value    ��ת���
     * @param error_info        Ӧ��Ĵ�����Ϣ
     * @param request_id        �������кţ�����ƥ����Ӧ�����û��Զ���
     */
    virtual void OnTransferFundBetweenSecuidRsp(int64_t transfer_value, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯETF������Ϣ����Ӧ��ÿ�η���һ��ETF��Ϣ
     *
     * @param etf_detail    ETF������Ϣ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryETFRsp(ETFDetail* etf_detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯһ��ETF��Ʊ���ӵ���Ӧ��ÿ�η���ETF��һ����Ʊ��Ϣ
     *
     * @param etf_stock_detail      ETF��һ����Ʊ��Ϣ
     * @param error_info            Ӧ��Ĵ�����Ϣ
     * @param request_id            ��Ӧ����ʱ��������к�
     * @param is_last               �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str				���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryETFStockRsp(ETFStockDetail* etf_stock_detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����ί�������ص�
     *
     * @param detail        ����ί����������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnQueryMaxOrderQtyRsp(MaxOrderQtyDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ�¹ɿ��깺��ȵ���Ӧ
     *
     * @param detail        �¹ɿ��깺�������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryIPOMaxPurchaseRsp(IPOMaxPurchaseDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
     * ��ѯ�¹ɵ���Ӧ
     *
     * @param detail        �¹�����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryIPOStockRsp(IPOStockDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ֤ȯ��Ϣ����Ӧ
     *
     * @param detail            ֤ȯ��Ϣ
     * @param error_info        Ӧ��Ĵ�����Ϣ
     * @param request_id        ��Ӧ����ʱ��������к�
     * @param is_last           �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQuerySecurityBaseInfoRsp(SecurityBaseInfo* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
     * ����Ʒת��ת��Ӧ��ص�
     *
     * @param rsp           ����Ʒת��ת��Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnCreditMortgageInOutRsp(CreditMortgageInOutRsp* rsp, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ȯ��ȯӦ��ص�
     *
     * @param rsp           ��ȯ��ȯӦ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnCreditStockBackRsp(CreditStockBackRsp* rsp, ErrorInfo* error_info,
        int request_id);

    /**
     * ֱ�ӻ���Ӧ��ص�
     *
     * @param rsp           ֱ�ӻ���Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnCreditPayBackRsp(CreditPayBackRsp* rsp, ErrorInfo* error_info, int request_id);

    /**
     * ָ����Լֱ�ӻ���
     *
     * @param rsp           ������Ϣ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ���
     */
    virtual void OnCreditPayBackByOrderRsp(CreditPayBackRsp* rsp, ErrorInfo* error_info,
        int request_id);

    /**
     * ���ñ��ȯӦ��ص�
     *
     * @param detail        ���ñ��ȯ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditStockRsp(CreditStockDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����Ʒȯ�ص�
     *
     * @param detail        ����Ʒȯ��Ϣ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditMortgageHoldRsp(CreditMortgageHoldDetail* detail,
        ErrorInfo* error_info, int request_id, bool is_last,
        const char* pos_str);

    /**
     * �����ʲ���ѯӦ��ص�
     *
     * @param detail        �����ʲ�����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryCreditAssetsRsp(CreditAssetsDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ���ʺ�ԼӦ��ص�
     *
     * @param detail        ���ʺ�Լ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditFinanceRsp(CreditFinanceDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ��ȯ��ԼӦ��ص�
     *
     * @param detail        ��ȯ��Լ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditShortsellRsp(CreditShortsellDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ�ɻ����ʸ�ծ���Ӧ��ص�
     *
     * @param detail        �ɻ��������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryCreditRepayAmountRsp(CreditRepayAmountDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ�ɻ���ȯ��ծ����Ӧ��ص�
     *
     * @param detail        �ɻ���ȯ��ծ��������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditRepayStockRsp(CreditRepayStockDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����ȯ��������Ӧ��ص�
     *
     * @param rsp               ��ѯ����ȯ��������Ӧ��
     * @param error_info        Ӧ��Ĵ�����Ϣ
     * @param request_id        �������кţ�����ƥ����Ӧ�����û��Զ���
     * @param is_last           �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str           ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditSecuritySellQtyRsp(CreditSecuritySellQtyRsp* rsp,
        ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ�˻�����Ȩ�޻ص�
     *
     * @param rsp           ��ѯ����Ȩ��Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnQuerySecuidRightRsp(QrySecuidRightRsp* rsp, ErrorInfo* error_info,
        int request_id);

    // ����ͨ�����ͨ���нӿ�
    /**
     * ��ѯ����ͨ�ο����ʵ���Ӧ
     *
     * @param detail        ����ͨ�ο���������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryHKRateRsp(HKRateDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last);

    /**
     * ��ѯ����ͨ���ȯ����Ӧ
     *
     * @param detail        ����ͨ���ȯ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryHKStockRsp(HKStockDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ����ͨ���ʽ���ʲ�����Ӧ
     *
     * @param detail        ����ͨ���ʽ���ʲ�����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryHKFundRsp(HKFundDetail* detail, ErrorInfo* error_info, int request_id);

    /**
     * ��ѯ����ͨ��С�۲����Ӧ
     *
     * @param detail        ����ͨ��С�۲�����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryHKMinPriceUnitRsp(HKMinPriceUnitDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����ͨ������������Ӧ
     *
     * @param detail        ����ͨ������������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryHKTradeCalendarRsp(HKTradeCalendarDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
     * ��ѯ��ȯ��ϸӦ��
     *
     * @param detail        ��ȯ��ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryLockSecurityDetailRsp(LockSecurityDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * չ��Ӧ��
     *
     * @param rsp           չ��Ӧ������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnExtendLockSecurityRsp(ExtendLockSecurityRsp* rsp, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ��ȯչ������Ӧ��
     *
     * @param detail        չ����ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryLockSecurityExtensionRsp(LockSecurityExtensionDetail* detail,
        ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ�ʽ�ת��ˮ����Ӧ
     *
     * @param detail        �ʽ�ת��ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryTransferFundHistoryRsp(TransferFundDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
    * ��ѯ���ո�ծ��ˮ����Ӧ
    *
    * @param detail        ��ծ��ˮ��ϸ����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryCreditDebtsFlowRsp(CreditDebtsFlowDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
    * ��ѯ�����ʽ���ˮ����Ӧ
    *
    * @param detail        �ʽ���ˮ��ϸ����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryCreditAssetFlowRsp(CreditAssetFlowDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
    * ��ѯ���ÿͻ�������ȯ��Լ����Ӧ
    *
    * @param detail        ���ÿͻ�������ȯ��Լ��ϸ����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryCreditDebtsRsp(CreditDebtsDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ΢����Ӧ��
     *
     * @param rsp           ΢����Ӧ������
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnMicroServiceRsp(MicroServiceRsp* rsp, int request_id);

    /**
     * ��ѯ�����˺����Ӧ��ص�
     *
     * @param detail        ���������ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryBankBalanceRsp(BankBalanceDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ������������б�Ӧ��
     *
     * @param detail        �����б���ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     *
     * @return              �ɹ�����0��ʧ�ܷ��ش����룬ͨ��GetApiLastError��ȡ������Ϣ
     */
    virtual void OnQueryBankInfoRsp(BankInfoDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last);

    /**
     * ��֤ת��Ӧ��ص�
     *
     * @param rsp           ��֤ת��Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnBankSecTransferRsp(BankSecTransferRsp* rsp, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ������֤ת�����ݻص�
     *
     * @param rsp           ������֤ת������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryBankSecTransferRsp(BankSecTransferDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
     * ��ѯ��֤ת����ʷ���ݻص�
     *
     * @param detail        ��֤ת����ʷ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryHisBankSecTransferRsp(HisBankSecTransferDetail* detail,
        ErrorInfo* error_info, int request_id, bool is_last,
        const char* pos_str);

    /**
     * �����ʽ�תӦ��ص�
     *
     * @param detail        �����ʽ�תӦ����ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnFundAccountTransferRsp(FundAccountTransferRsp* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ���������ʽ��˺�֮���ʽ�תӦ��ص�
     *
     * @param detail        �����ʽ�ת��ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnQueryFundAccountTransferRsp(FundAccountTransferDetail* detail,
        ErrorInfo* error_info, int request_id);

    /**
     * ��ѯ��ʷί�лص�
     *
     * @param detail        ��ʷί����ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryHisOrderRsp(HisOrderDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ��ʷ�ɽ�Ӧ��ص�
     *
     * @param detail        ��ʷ�ɽ���ϸ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryHisTradeRsp(HisTradeDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ���Ӧ��ص� -- ΢����򻯰�
     *
     * @param detail        �����ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryDeliveryOrderRsp(DeliveryOrderDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ���˵���ѯӦ��ص� -- ΢����򻯰�
     *
     * @param detail        ���˵���ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryStateOrderRsp(StateOrderDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
    * ��ѯ���(�ֱ�)Ӧ��ص� -- ���н�����ϸ��
    *
    * @param detail        �����ϸ
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryExchangeListsRsp(ExchangeDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * �޸��������Ӧ
     *
     * @param rsp           �޸�����Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     */
    virtual void OnModifyPasswordRsp(ModifyPasswordRsp* rsp, ErrorInfo* error_info,
        int request_id);

    /**
    * ��ѯ�����ϢӦ��ص�
    *
    * @param detail        �����Ϣ����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryPHXXRsp(QueryPHXXRecord* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
    * ��ѯ��ǩ��ϢӦ��ص�
    *
    * @param detail        ��ǩ��Ϣ����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryZQXXRsp(QueryZQXXRecord* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ��ȯ��ͬӦ��
     *
     * @param detail        ��ȯ��ͬ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryLockSecurityContractRsp(LockSecurityContractDetail* detail,
        ErrorInfo* error_info, int request_id, bool is_last,
        const char* pos_str);

    /**
     * ��ѯ���ú�ͬӦ��
     *
     * @param detail        ���ú�ͬ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnQueryCreditContractRsp(CreditContractDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ������ȯ��Լ������ϢӦ��
     *
     * @param detail        ������ȯ��Լ������Ϣ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditDebtsCollectRsp(CreditDebtsCollectDetail* detail,
        ErrorInfo* error_info, int request_id, bool is_last,
        const char* pos_str);

    /**
     * ��ѯ������ȯ��������Ӧ��
     *
     * @param detail        ������ȯ������������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnQueryCreditDataRsp(CreditDataDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ����Ԥ���ں�ԼӦ��
     *
     * @param detail        ����Ԥ���ں�Լ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryPreMaturityDebtsRsp(PreMaturityDebtsDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ����Ԥ���ں�Լչ��Ӧ��
     *
     * @param detail        ����Ԥ���ں�Լչ��Ӧ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnExtendPreMaturityDebtsRsp(ExtendPreMaturityDebtsRsp* detail,
        ErrorInfo* error_info, int request_id);

    /**
     * ��ѯ����Ԥ���ں�Լչ��Ӧ��
     *
     * @param detail        ����Ԥ���ں�Լչ������
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryPreMaturityDebtsExtensionRsp(PreMaturityDebtsExtensionDetail* detail,
        ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
     * ��ѯ����ͶƱ�鰸Ӧ��
     *
     * @param rsp           ����ͶƱ�鰸����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryVoteProposalRsp(VoteProposalDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
     * ��ѯ����ͶƱ��ͶƱ��Ӧ��
     *
     * @param detail        ����ͶƱ��ͶƱ��
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
     */
    virtual void OnQueryCreditVoteCountRsp(CreditVoteCountDetail* detail, ErrorInfo* error_info,
        int request_id);

    /**
     * ��ѯ����ͶƱ���Ӧ��
     *
     * @param detail        ����ͶƱ����
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryCreditVoteRsp(CreditVoteDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����ͶƱ�ͻ�Ȩ��Ӧ��
     *
     * @param detail        ����ͶƱ�ͻ�Ȩ����ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryNetVoteRightsRsp(NetVoteRightsDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����ͶƱ���Ӧ��
     *
     * @param detail        ����ͶƱ�����ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
     */
    virtual void OnQueryNetVoteResultRsp(NetVoteResultDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
     * ��ѯ����ͶƱ��ͶƱ����Ӧ��
     *
     * @param detail        ����ͶƱ��ͶƱ������ϸ
     * @param error_info    Ӧ��Ĵ�����Ϣ
     * @param request_id    ��Ӧ����ʱ��������к�
     * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
     */
    virtual void OnQueryNetVoteCountRsp(NetVoteCountDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last);

    /**
    * ��Ʊ���жȲ�ѯӦ��
    *
    * @param detail        ��Ʊ���ж���ϸ
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryStkConcentrationRsp(StkConcentrationDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
    * ��ѯ����ͨ��ʷί����ϸ����Ӧ
    *
    * @param detail        ��ʷί����ϸ����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryHKHisOrderRsp(HKHisOrderDetail* detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
    * ��ѯ��ȡ�ʽ����Ӧ
    *
    * @param detail        ��ȡ�ʽ�����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    */
    virtual void OnQueryWithdrawCashRsp(WithdrawCashRecord* detail, ErrorInfo* error_info, int request_id);

    /**
    * ��ѯ����ͶƱί��Ӧ��
    *
    * @param detail        ����ͶƱί������
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    �������кţ�����ƥ����Ӧ�����û��Զ��壬��0
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryNetVoteOrderRsp(NetVoteOrderDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
    * ��ѯ����ί�б��еĻ��ܳɽ���Ϣ����Ӧ��һ�η���һ���ɽ�����
    *
    * @param trade_detail  �ɽ�����
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
    * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
    */
    virtual void OnQueryTradeTotalRsp(TradeDetail* trade_detail, ErrorInfo* error_info, int request_id,
        bool is_last, const char* pos_str);

    /**
    * ETF �Ϲ� ������Ӧ��
    *
    * @param order_rsp     ETF �Ϲ� ������Ӧ��
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    */
    virtual void OnETFSubscriptCancelRsp(ETFSubscriptCancelRsp* order_rsp, ErrorInfo* error_info,
        int request_id);

    /**
    * ����ͶƱί�е���Ӧ
    *
    * @param order_rsp     ����ͶƱί��Ӧ��
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    */
    virtual void OnNetVoteOrderRsp(NetVoteOrderRsp* order_rsp, ErrorInfo* error_info,
        int request_id);

    /**
    * ����ͶƱί�е���Ӧ
    *
    * @param order_rsp     ����ͶƱί��Ӧ��
    * @param error_info    Ӧ��Ĵ�����Ϣ
    * @param request_id    ��Ӧ����ʱ��������к�
    */
    virtual void OnCreditNetVoteOrderRsp(CreditNetVoteOrderRsp* order_rsp, ErrorInfo* error_info,
        int request_id);

    /**
       * �ͻ��ʽ��ѯӦ��ص���΢��������
       *
       * @param detail        ��ϸ��Ϣ
       * @param error_info    Ӧ��Ĵ�����Ϣ
       * @param request_id    ��Ӧ����ʱ��������к�
       * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
       * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
       */
    virtual void OnQueryMSCashRsp(MSCashDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
       * �ͻ��ֲֲ�ѯӦ��ص���΢��������
       *
       * @param detail        ��ϸ��Ϣ
       * @param error_info    Ӧ��Ĵ�����Ϣ
       * @param request_id    ��Ӧ����ʱ��������к�
       * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
       * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
       */
    virtual void OnQueryMSPositionsRsp(MSPositionsDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    /**
       * ���ø�ծ��ˮ��ѯӦ��ص���΢��������
       *
       * @param detail        ��ϸ��Ϣ
       * @param error_info    Ӧ��Ĵ�����Ϣ
       * @param request_id    ��Ӧ����ʱ��������к�
       * @param is_last       �Ƿ��Ǳ�����������һ����Ӧ
       * @param pos_str       ���β�ѯ���һ����¼�Ķ�λ����������һ�β�ѯ
       */
    virtual void OnQueryMSCreditDebtsFlowRsp(MSCreditDebtsFlowDetail* detail, ErrorInfo* error_info,
        int request_id, bool is_last, const char* pos_str);

    //-------------------------------------------------------------------------------------
    //data���ص������������ֵ�
    //error���ص������Ĵ����ֵ�
    //id������id
    //last���Ƿ�Ϊ��󷵻�
    //i������
    //-------------------------------------------------------------------------------------
    virtual void onDisconnect() {};

    virtual void onError(const dict& error, int request_id) {};

    virtual void onRiskNotify(const dict& data) {};

    virtual void onFailBackNotify(const dict& data) {};

    virtual void onLogin(const dict& data, const dict& error) {};

    virtual void onTradeReport(const dict& data) {};

    virtual void onOrderStatus(const dict& data) {};

    virtual void onOrderRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onCancelRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryOrderRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryTradeRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryPositionRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCashRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryJZJYAvailFundRsp(int64_t avail_balance, const dict& error, int request_id) {};

    virtual void onTransferFundInAndOutRsp(int64_t transfer_value, const dict& error, int request_id) {};

    virtual void onTransferFundBetweenSecuidRsp(int64_t transfer_value, const dict& error, int request_id) {};

    virtual void onQueryETFRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryETFStockRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryMaxOrderQtyRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryIPOMaxPurchaseRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryIPOStockRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQuerySecurityBaseInfoRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onCreditMortgageInOutRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onCreditStockBackRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onCreditPayBackRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onCreditPayBackByOrderRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryCreditStockRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditMortgageHoldRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditAssetsRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryCreditFinanceRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditShortsellRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditRepayAmountRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryCreditRepayStockRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditSecuritySellQtyRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQuerySecuidRightRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryHKRateRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryHKStockRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryHKFundRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryHKMinPriceUnitRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryHKTradeCalendarRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryLockSecurityDetailRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onExtendLockSecurityRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryLockSecurityExtensionRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryTransferFundHistoryRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryCreditDebtsFlowRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditAssetFlowRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditDebtsRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onMicroServiceRsp(const dict& data, int request_id) {};

    virtual void onQueryBankBalanceRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryBankInfoRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onBankSecTransferRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryBankSecTransferRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryHisBankSecTransferRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onFundAccountTransferRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryFundAccountTransferRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryHisOrderRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryHisTradeRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryDeliveryOrderRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryStateOrderRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryExchangeListsRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onModifyPasswordRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryPHXXRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryZQXXRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryLockSecurityContractRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditContractRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryCreditDebtsCollectRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryCreditDataRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryPreMaturityDebtsRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onExtendPreMaturityDebtsRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryPreMaturityDebtsExtensionRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryVoteProposalRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryCreditVoteCountRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryCreditVoteRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryNetVoteRightsRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryNetVoteResultRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryNetVoteCountRsp(const dict& data, const dict& error, int request_id, bool last) {};

    virtual void onQueryStkConcentrationRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryHKHisOrderRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryWithdrawCashRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryNetVoteOrderRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryTradeTotalRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onETFSubscriptCancelRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onNetVoteOrderRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onCreditNetVoteOrderRsp(const dict& data, const dict& error, int request_id) {};

    virtual void onQueryMSCashRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryMSPositionsRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    virtual void onQueryMSCreditDebtsFlowRsp(const dict& data, const dict& error, int request_id, bool last, string pos_str) {};

    //-------------------------------------------------------------------------------------
    //req:���������������ֵ�
    //-------------------------------------------------------------------------------------
	void setLogConfig(string log_path);

    void createTraderApi();

    void release();

    int exit();

    string getApiVersion();

	void setCriticalMsgLog(bool enable);

	void setLoginRetryCount(int login_retry_count);

	void setLoginRetryInterval(int login_retry_interval);

	void setReconnectConfig(int max_retry_count, int min_interval, int max_interval);

    dict getApiLastError();

    int login(string svr_ip, int svr_port, const dict& req, string terminal_info);

    int getCounterType();

    int getSecuidInfo(const dict& req, int count);

    int getAllSecuidInfo(const dict& req, int count);

    int getApiLocalAddr(const dict& req);

    int order(const dict& req, int request_id);

    int batchOrder(const dict& req, int count, int request_id);

    int cancelOrder(const dict& req, int request_id);

    int batchCancelOrder(const dict& req, int count, int request_id);

    int batchCancelAllOrder(const dict& req, int request_id);

    int queryOrder(const dict& req, int request_id);

    int queryOrderByCode(const dict& req, int request_id);

    int queryOrders(const dict& req, int request_id);

    int queryTradeByOrderId(const dict& req, int request_id);

    int queryTradeByCode(const dict& req, int request_id);

    int queryTrades(const dict& req, int request_id);

    int queryETFTrades(const dict& req, int request_id);

    int queryPosition(const dict& req, int request_id);

    int queryPositions(const dict& req, int request_id);

    int queryCash(const dict& req, int request_id);

    int queryJZJYAvailFund(int request_id);

    int transferFundInAndOut(const dict& req, int request_id);

    int transferFundBetweenSecuid(const dict& req, int request_id);

    int queryETFs(const dict& req, int request_id);

    int queryETFStocks(const dict& req, int request_id);

    int queryMaxOrderQty(const dict& req, int request_id);

    int queryIPOMaxPurchase(int request_id);

    int queryIPOStock(const dict& req, int request_id);

    int querySecurityBaseInfo(const dict& req, int request_id);

    int creditMortgageInOut(const dict& req, int request_id);

    int creditStockBack(const dict& req, int request_id);

    int creditPayBack(const dict& req, int request_id);

    int creditPayBackByOrder(const dict& req, int request_id);

    int queryCreditStock(const dict& req, int request_id);

    int queryCreditMortgageHold(const dict& req, int request_id);

    int queryCreditAssets(int request_id);

    int queryCreditFinance(const dict& req, int request_id);

    int queryCreditShortsell(const dict& req, int request_id);

    int queryCreditRepayAmount(int request_id);

    int queryCreditRepayStock(const dict& req, int request_id);

    int queryCreditSecuritySellQty(const dict& req, int request_id);

    int querySecuidRight(const dict& req, int request_id);

    int queryHKRate(const dict& req, int request_id);

    int queryHKStock(const dict& req, int request_id);

    int queryHKFund(int request_id);

    int queryHKMinPriceUnit(const dict& req, int request_id);

    int queryHKTradeCalendar(const dict& req, int request_id);

    int queryLockSecurityDetail(const dict& req, int request_id);

    int extendLockSecurity(const dict& req, int request_id);

    int queryLockSecurityExtension(const dict& req, int request_id);

    int queryTransferFundHistory(int request_id);

    int queryCreditDebtsFlow(const dict& req, int request_id);

    int queryCreditAssetFlow(const dict& req, int request_id);

    int queryCreditDebts(const dict& req, int request_id);

    int doMicroServiceReq(const dict& req, int request_id);

    int queryBankBalance(const dict& req, int request_id);

    int queryBankInfo(const dict& req, int request_id);

    int bankSecTransfer(const dict& req, int request_id);

    int queryBankSecTransfer(const dict& req, int request_id);

    int queryHisBankSecTransfer(const dict& req, int request_id);

    int fundAccountTransfer(const dict& req, int request_id);

    int queryFundAccountTransfer(const dict& req, int request_id);

    int queryHisOrders(const dict& req, int request_id);

    int queryHisTrades(const dict& req, int request_id);

    int queryDeliveryOrders(const dict& req, int request_id);

    int queryStateOrders(const dict& req, int request_id);

    int queryExchangeLists(const dict& req, int request_id);

    int modifyPassword(const dict& req, int request_id);

    int queryPHXX(const dict& req, int request_id);

    int queryZQXX(const dict& req, int request_id);

    int queryLockSecurityContract(const dict& req, int request_id);

    int queryCreditContract(int request_id);

    int queryCreditDebtsCollect(const dict& req, int request_id);

    int queryCreditData(const dict& req, int request_id);

    int queryPreMaturityDebts(const dict& req, int request_id);

    int extendPreMaturityDebts(const dict& req, int request_id);

    int queryPreMaturityDebtsExtension(const dict& req, int request_id);

    int queryVoteProposal(const dict& req, int request_id);

    int queryCreditVoteCount(const dict& req, int request_id);

    int queryCreditVote(const dict& req, int request_id);

    int queryNetVoteRights(const dict& req, int request_id);

    int queryNetVoteResult(const dict& req, int request_id);

    int queryNetVoteCount(const dict& req, int request_id);

    int appointContractSellStockRepay(const dict& req, int request_id);

    int queryStkConcentration(const dict& req, int request_id);

    int queryHKHisOrders(const dict& req, int request_id);

    int queryWithdrawCash(const dict& req, int request_id);

    int queryTradeListTotal(const dict& req, int request_id);

    int eTFSubscriptCancel(const dict& req, int request_id);

    int queryNetVoteOrder(const dict& req, int request_id);

    int netVoteOrder(const dict& req, int request_id, string terminal_info);

    int creditNetVoteOrder(const dict& req, int request_id, string terminal_info);

    int queryMSCash(const dict& req, int request_id);

    int queryMSPositions(const dict& req, int request_id);

    int queryMSCreditDebtsFlow(const dict& req, int request_id);

};
