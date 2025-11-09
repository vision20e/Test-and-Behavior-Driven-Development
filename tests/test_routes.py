    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_read_a_product(self):
        """It should Read a single Product"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)
        self.assertEqual(data["description"], test_product.description)

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_a_product(self):
        """It should Update an existing Product"""
        test_product = self._create_products(1)[0]
        new_description = "Updated product description"
        test_product.description = new_description
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}",
            json=test_product.serialize()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], new_description)

    # ----------------------------------------------------------
    # TEST DELETE
    # ----------------------------------------------------------
    def test_delete_a_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it’s gone
        get_response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------------------------------------------
    # TEST LIST ALL
    # ----------------------------------------------------------
    def test_list_all_products(self):
        """It should List all Products"""
        self._create_products(3)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    # ----------------------------------------------------------
    # TEST FIND BY NAME
    # ----------------------------------------------------------
    def test_query_products_by_name(self):
        """It should Query Products by Name"""
        products = self._create_products(3)
        name = products[0].name
        response = self.client.get(BASE_URL, query_string=f"name={name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]["name"], name)

    # ----------------------------------------------------------
    # TEST FIND BY CATEGORY
    # ----------------------------------------------------------
    def test_query_products_by_category(self):
        """It should Query Products by Category"""
        products = self._create_products(5)
        category = products[0].category.name
        response = self.client.get(BASE_URL, query_string=f"category={category}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["category"] == category for p in data))

    # ----------------------------------------------------------
    # TEST FIND BY AVAILABILITY
    # ----------------------------------------------------------
    def test_query_products_by_availability(self):
        """It should Query Products by Availability"""
        products = self._create_products(4)
        available_count = len([p for p in products if p.available])
        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["available"] is True for p in data))
        self.assertTrue(len(data) <= available_count)
