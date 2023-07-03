package pers.Steven.shoppingManagementSystem.universalFunction;

public class Item {
    private String name;
    private String manufacturer;
    private String manuDate;
    private String type;//型号
    private float buyingPrice;
    private float sellPrice;
    private int num;

    public Item(String originalData) {
        String[] property;
        if (originalData != null) {
            property = originalData.split("~");//得到商品的各项内容
            name = property[0];
            manufacturer = property[1];
            manuDate = property[2];
            type = property[3];
            buyingPrice = Float.parseFloat(property[4]);
            sellPrice = Float.parseFloat(property[5]);
            num = Integer.parseInt(property[6]);
        }
    }

    public Item() {
    }

    public void showAllMessageForAdmin() {
        System.out.println("---------商品信息---------");
        System.out.println("商品名称：" + name);
        System.out.println("生产厂家：" + manufacturer);
        System.out.println("生产日期：" + manuDate);
        System.out.println("型号：" + type);
        System.out.println("进货价：" + buyingPrice);
        System.out.println("零售价：" + sellPrice);
        System.out.println("数量：" + num);
        System.out.println("-------------------------\n");
    }

    public void showAllMessageForUser() {
        System.out.println("---------商品信息---------");
        System.out.println("商品名称：" + name);
        System.out.println("生产厂家：" + manufacturer);
        System.out.println("生产日期：" + manuDate);
        System.out.println("型号：" + type);
        System.out.println("价格：" + sellPrice);
        System.out.println("数量：" + num);
        System.out.println("-------------------------\n");
    }

    public String getWriteInString() {
        String formattedString = name + "~" + manufacturer + "~" + manuDate + "~" + type + "~" + buyingPrice + "~" + sellPrice + "~" + num;
        return formattedString;
    }

    public void copy(Item another) {
        name = another.getName();
        manufacturer = another.getManufacturer();
        manuDate = another.getManuDate();
        type = another.getType();//型号
        buyingPrice = another.getBuyingPrice();
        sellPrice = another.getSellPrice();
        num = another.getNum();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getManuDate() {
        return manuDate;
    }

    public void setManuDate(String manuDate) {
        this.manuDate = manuDate;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public float getBuyingPrice() {
        return buyingPrice;
    }

    public void setBuyingPrice(String buyingPrice) {
        this.buyingPrice = Float.parseFloat(buyingPrice);
    }

    public float getSellPrice() {
        return sellPrice;
    }

    public void setSellPrice(String sellPrice) {
        this.sellPrice = Float.parseFloat(sellPrice);
    }

    public int getNum() {
        return num;
    }

    public void setNum(String num) {
        this.num = Integer.parseInt(num);
    }

    public void setNum(int num) {
        this.num = num;
    }
}
