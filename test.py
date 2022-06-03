    # post = driver.find_element(By.CSS_SELECTOR, '.text_exposed_root')
    # print(post.text)
    # context = driver.find_element(By.CSS_SELECTOR,"span.text_exposed_show")
    # print(context.get_attribute("outerHTML"))

def bt4():
    response = requests.get('https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Ftaiwanauction%2Fposts%2F5096405560436133')
    soup = BeautifulSoup(response.text, "html.parser")
    resoult=soup.find_all(class_="text_exposed_root")
    print(resoult)